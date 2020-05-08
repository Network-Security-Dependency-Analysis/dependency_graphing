import json
import os
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = "/Users/matt/Downloads/tmp"

for filename in os.listdir(DATA_DIR):
	try:
		# Retrieve the json data on dependencies
		with open(os.path.join(DATA_DIR, filename)) as f:
			data = json.load(f)

		domains = []
		a_count = []
		script_count = []
		link_count = []
		iframe_count = []
		video_count = []
		audio_count = []
		img_count = []
		embed_count = []
		object_count = []

		for ext_domain in data["external_domains"]:
			if data["external_domains"][ext_domain]["resources"]["total"] > 10:
				domains.append(ext_domain)
				a_count.append(data["external_domains"][ext_domain]["resources"]["a"])
				script_count.append(data["external_domains"][ext_domain]["resources"]["script"])
				link_count.append(data["external_domains"][ext_domain]["resources"]["link"])
				iframe_count.append(data["external_domains"][ext_domain]["resources"]["iframe"])
				video_count.append(data["external_domains"][ext_domain]["resources"]["video"])
				audio_count.append(data["external_domains"][ext_domain]["resources"]["audio"])
				img_count.append(data["external_domains"][ext_domain]["resources"]["img"])
				embed_count.append(data["external_domains"][ext_domain]["resources"]["embed"])
				object_count.append(data["external_domains"][ext_domain]["resources"]["object"])

		plt.rcdefaults()
		fig, ax = plt.subplots()
		fig.set_size_inches(24, 16)
		y_pos = np.arange(len(domains))

		ax.barh(y_pos, a_count, color="#FF5733", label="a tags")
		ax.barh(y_pos, script_count, left=a_count, color="#FFBD33", label="script tags")
		ax.barh(y_pos, link_count, left=script_count, color="#F6FF33", label="link tags")
		ax.barh(y_pos, iframe_count, left=link_count, color="#39FF33", label="iframe tags")
		ax.barh(y_pos, video_count, left=iframe_count, color="#33FFBD", label="video tags")
		ax.barh(y_pos, audio_count, left=video_count, color="#0205B6", label="audio tags")
		ax.barh(y_pos, img_count, left=audio_count, color="#3380FF", label="img tags")
		ax.barh(y_pos, embed_count, left=img_count, color="#B233FF", label="embed tags")
		ax.barh(y_pos, object_count, left=embed_count, color="#FF33E6", label="object tags")

		ax.set_yticks(y_pos)
		ax.set_yticklabels(domains)
		ax.set_xlabel("Number of References", fontsize=18)
		ax.set_ylabel("Domains Referenced (>10 refs)", fontsize=18)
		ax.set_title("External domain references for " + data["top_domain"], fontsize=24, fontweight="bold")
		ax.legend()

		plt.savefig(data["top_domain"] + ".png")
	except:
		pass
