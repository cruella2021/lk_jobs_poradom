from jobs import info_doc, image_stage, doc_pdf, start_settings
import time

def main():
	
	start_settings.insert_default_settings()
	new_Doc = info_doc.Doc_and_stage()
	new_Doc.main()
	
	image_stage.delete_image()
	image_stage.load_images()
	image_stage.update_sum_image_in_stage()
	image_stage.upload_image_from_srv()
	doc_pdf.get_pdf_for_doc()
	doc_pdf.get_pdf_for_dop()

#main()
#while True:
	#main()
	#print('================')
	#time.sleep(3*60*60)
	#print('=====SLEEP=====')
	
