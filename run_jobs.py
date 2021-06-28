#from jobs import info_doc, image_stage, doc_pdf, start_settings
import sys
from jobs import start_settings, settings_connect, info_doc, image_stage,doc_pdf
import time

fl_exit = False

start_settings.insert_default_settings()

defaul_settings = settings_connect.Config()

if defaul_settings.ERROR:
	print(defaul_settings.ERROR_TEXT)
	sys.exit()

#new_Doc 	= info_doc.Doc_and_stage(defaul_settings)
#new_Image 	= image_stage.Load_update_image(defaul_settings)
new_Pdf		= doc_pdf.Load_update_pdf(defaul_settings)

def main():
#	new_Doc.main()
#	new_Image.main()
	new_Pdf.main()

main()
#while True:
	#main()
	#print('================')
	#time.sleep(3*60*60)
	#print('=====SLEEP=====')
	
