from jobs import info_doc, image_stage, doc_pdf, start_settings
import time

from jobs import settings_connect

start_settings.insert_default_settings()

defaul_settings = settings_connect.Config()

new_Doc = info_doc()
new_Doc.set_settings(defaul_settings)
new_Doc.Doc_and_stage()

new_Image 	= image_stage()
new_Image.set_settings(defaul_settings)
new_Image.Load_update_image()

newPDF = doc_pdf()
newPDF.set_settings(defaul_settings)
newPDF.Load_update_pdf()


def main():
	
	new_Doc.main()
	new_Image.main()
	newPDF.main()

#main()
#while True:
	#main()
	#print('================')
	#time.sleep(3*60*60)
	#print('=====SLEEP=====')
	
