from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import sys
import time
import numpy as np
import logging
import requests

import tensorflow as tf

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

# Validation annotation files
tf.flags.DEFINE_string(
    "anno_files_path", 
    os.path.dirname(os.path.abspath(__file__)) + "\\anno_list_mscoco_crVal_m_RNN.npy",
    "Validation file annotations, multipy files should be seperated by ':'")

tf.logging.set_verbosity(tf.logging.INFO)

def main():
	pred_sentences = []
	num_decode = 0
	annos = np.load(FLAGS.anno_files_path).tolist()

	for anno in annos:
		filename = anno['file_name']
		filepath = os.path.dirname(os.path.realpath(__file__)) + "\\data\\raw-data\\val2014\\" + filename
		
		r = requests.post(
    		"https://api.deepai.org/api/neuraltalk",
	    	files={
	    	
			'image': open(filepath, 'rb')
	    	  
	    	
			},
	    	headers={'api-key': '2f5d13eb-75af-4ec7-97de-0800b74ee203'}
		)

		sentence_coco = {}
		sentence_coco['image_id'] = anno['id']
		sentence_coco['caption'] = r.json()['output']

		pred_sentences.append(sentence_coco)
		
		num_decode += 1
		if num_decode % 10 == 0:
			logger.info('%d images are decoded' % num_decode)


	pred_path = os.path.dirname(os.path.realpath(__file__)) + "\\predictions_nt2.json"
	result_path = os.path.dirname(os.path.realpath(__file__)) + "\\results_nt2.txt"

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
	main()	