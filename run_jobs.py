from jobs import info_doc, image_stage, doc_pdf, start_settings
import time

start_settings.insert_default_settings()

new_Doc 	= info_doc.Doc_and_stage()
new_Stage 	= image_stage.Load_update_image()
newPDF 		= doc_pdf.Load_update_pdf()


def main():
	
	new_Doc.main()
	new_Stage.main()
	newPDF.main()

#main()
#while True:
	#main()
	#print('================')
	#time.sleep(3*60*60)
	#print('=====SLEEP=====')
	
