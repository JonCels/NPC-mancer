import pdfrw as p

characterSheetTemplatePDF = "template.pdf"
characterSheetOutputPDF = "output.pdf"

templatePDF = p.PdfReader(characterSheetTemplatePDF)

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

# for page in templatePDF.pages:
#     annotations = page[ANNOT_KEY]
#     for annotation in annotations:
#         if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
#             if annotation[ANNOT_FIELD_KEY]:
#                 key = annotation[ANNOT_FIELD_KEY][1:-1]
#                 print(key)

#Takes the pdf given as inputPDF, adds the data specified in characterData, and creates a new pdf with the data given and the name given as outputPDF
def fillPDF(inputPDF, outputPDF, characterData):
    templatePDF = p.PdfReader(inputPDF)
    for page in templatePDF.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in characterData.keys():
                        if type(characterData[key]) == bool:
                            if characterData[key] == True:
                                annotation.update(p.PdfDict(
                                    AS=p.PdfName('Yes')))
                        else:
                            annotation.update(
                                p.PdfDict(V='{}'.format(characterData[key]))
                            )
                            annotation.update(p.PdfDict(AP=''))
    p.PdfWriter().write(outputPDF, templatePDF)


characterData = {
    'ClassLevel': 'Ranger, ' + str(5),
    'Background': 'urchin',
    'Race': 'High Elf',
    'STR': 13
}

fillPDF(characterSheetTemplatePDF, characterSheetOutputPDF, characterData)