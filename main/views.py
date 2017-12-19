
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

import requests
import os
import math
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__))+'\\im2txt\\')

import tensorflow as tf

import configuration
import inference_wrapper
from inference_utils import caption_generator
from inference_utils import vocabulary

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("checkpoint_path", os.path.dirname(os.path.abspath(__file__)) + "\\im2txt\\model\\train\\model.ckpt-2000000",
                       "Model checkpoint file or directory containing a "
                       "model checkpoint file.")
tf.flags.DEFINE_string("vocab_file", os.path.dirname(os.path.abspath(__file__)) + "\\im2txt\\word_counts.txt", "Text file containing the vocabulary.")
tf.logging.set_verbosity(tf.logging.INFO)

@csrf_exempt
def index(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		# img = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\media\\" + myfile.name, "rb")

		g = tf.Graph()
		with g.as_default():
			model = inference_wrapper.InferenceWrapper()
			restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
			                                           FLAGS.checkpoint_path)
		g.finalize()

		# Create the vocabulary.
		vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

		with tf.Session(graph=g) as sess:
			# Load the model from checkpoint.
			restore_fn(sess)

			# Prepare the caption generator. Here we are implicitly using the default
			# beam search parameters. See caption_generator.py for a description of the
			# available beam search parameters.
			generator = caption_generator.CaptionGenerator(model, vocab)

			with tf.gfile.GFile(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\media\\" + myfile.name, "rb") as f:
				image = f.read()
			captions = generator.beam_search(sess, image)
			# print (enumerate(captions))
			print("Captions for image %s:" % os.path.basename(myfile.name))
			for i, caption in enumerate(captions):
				print(caption.sentence)
				# Ignore begin and end words.
				sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
				sentence = " ".join(sentence)
				print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
				break

		# r = requests.post(
		#     "https://api.deepai.org/api/neuraltalk",
		#     files={
		    
		#     'image': img
		      
		    
		#     },
		#     headers={'api-key': '17b00d3b-69db-49f5-8931-1c4dc0945e25'}
		# )

		# print(r.json()['output'])
		
		data = {}
		data['caption'] = sentence
		json_data = json.dumps(data)
		return HttpResponse(json_data)
	# 	return render(request, 'main/index.html', {
	# 	    'uploaded_file_url': uploaded_file_url
	# 	    })
	# return render(request, 'main/index.html')