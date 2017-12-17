from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import json
import sys
import time
import numpy as np
import logging

import tensorflow as tf

import configuration
import inference_wrapper
from inference_utils import caption_generator
from inference_utils import vocabulary

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'\\TF-mRNN\\external\\coco-caption')
from pycocotools import coco
from pycocoevalcap import eval

logger = logging.getLogger('ExpMscoco')
formatter_log = "[%(asctime)s - %(filename)s:line %(lineno)4s] %(message)s"
logging.basicConfig(
    format=formatter_log,
    datefmt='%d %b %H:%M:%S')
logger.setLevel(logging.INFO)

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("checkpoint_path", ".\\model\\train\\model.ckpt-2000000",
                       "Model checkpoint file or directory containing a "
                       "model checkpoint file.")
tf.flags.DEFINE_string("vocab_file", ".\\word_counts.txt", "Text file containing the vocabulary.")

# Validation annotation files
tf.flags.DEFINE_string(
    "anno_files_path", 
    os.path.dirname(os.path.abspath(__file__)) + "\\anno_list_mscoco_crVal_m_RNN.npy",
    "Validation file annotations, multipy files should be seperated by ':'")

tf.logging.set_verbosity(tf.logging.INFO)

def main(_):
	g = tf.Graph()
	with g.as_default():
		model = inference_wrapper.InferenceWrapper()
		restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
		                                           FLAGS.checkpoint_path)
	g.finalize()

	# Create the vocabulary.
	vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

	with tf.Session(graph=g) as sess:
		restore_fn(sess)

		generator = caption_generator.CaptionGenerator(model, vocab)
		print ("here")
		pred_sentences = []
		num_decode = 0
		annos = np.load(FLAGS.anno_files_path).tolist()

		for anno in annos:
			filename = anno['file_name']
			filepath = os.path.dirname(os.path.realpath(__file__)) + "\\data\\raw-data\\val2014\\" + filename
			
			with tf.gfile.GFile(filepath, "rb") as f:
				image = f.read()

			captions = generator.beam_search(sess, image)
			for i, caption in enumerate(captions):
				# print(caption.sentence)
				# Ignore begin and end words.
				sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
				sentence = " ".join(sentence)
				
				sentence_coco = {}
				sentence_coco['image_id'] = anno['id']
				sentence_coco['caption'] = sentence

				pred_sentences.append(sentence_coco)
				# print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
				break
			
			num_decode += 1
			if num_decode % 100 == 0:
				logger.info('%d images are decoded' % num_decode)


		pred_path = os.path.dirname(os.path.realpath(__file__)) + "\\predictions.json"
		result_path = os.path.dirname(os.path.realpath(__file__)) + "\\results.txt"

		with open(pred_path, 'w') as fout:
			json.dump(pred_sentences, fout, indent=4, sort_keys=True)

		coco2 = coco.COCO(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'\\TF-mRNN\\external\\coco-caption\\annotations\\captions_val2014.json')
		cocoRes = coco2.loadRes(pred_path)

		cocoEval = eval.COCOEvalCap(coco2, cocoRes)
		cocoEval.params['image_id'] = cocoRes.getImgIds()
		cocoEval.evaluate()
    
		with open(result_path, 'w') as fout:
			for metric, score in cocoEval.eval.items():
				print('%s: %.3f' % (metric, score), file=fout)

if __name__ == "__main__":
	tf.app.run()	