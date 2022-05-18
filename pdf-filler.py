from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas as pdfCanvas
from reportlab.lib.pagesizes import A4
import math

numDigits = 4
numCol = 3
numRow = 7
maxPerPage = numCol * numRow
marginCol = 110
marginRow = 120
paddingCol = 190
paddingRow = 108
prefixes = ["TB", "PH", "LP", "AC"]
numPerPrefix = 100
numPrefixes = len(prefixes)
numTotalIds = numPerPrefix * numPrefixes
numPerPage = numRow * numCol
pageHeight = A4[1]

# Create the canvas to overlay.
pdfs = []

for index in range(numTotalIds):
    id = index % numPerPrefix
    pageId = index % numPerPage
    
    if (pageId == 0):
        print("Creating new canvas")
        b = BytesIO()
        c = pdfCanvas.Canvas(b, pagesize=A4)

    type = math.floor(index / numPerPrefix)
    prefix = prefixes[type]
    strId = str(id+1) # Convert to 1-index numbering.
    numZeroes = numDigits - len(strId)
    label = prefix + "0"*numZeroes + strId
    col = pageId % numCol
    row = math.floor(pageId / numCol) # Meant to be numCol.
    x = marginCol + paddingCol * col
    y = pageHeight - (marginRow + paddingRow * row)
    c.drawString(x, y, label)

    print(pageId, label)

    if (pageId == numPerPage-1 or index == numTotalIds-1):
        print("Saving canvas",len(pdfs))
        c.showPage()
        c.save()
        b.seek(0)
        p = PdfFileReader(b)
        pdfs.append(p)

    index += 1

print(pdfs)

# Get template PDF.
templatePdfPath = str(
    Path.home()
    / "Device Labels.pdf"
)

# Create output PDF.
print("Creating new PDF...")
outputPdf = PdfFileWriter()
for i, canvasPdf in enumerate(pdfs):
    print(i)
    templatePage = PdfFileReader(templatePdfPath).getPage(0)
    canvasPage = canvasPdf.getPage(0)
    templatePage.mergePage(canvasPage)
    outputPdf.addPage(templatePage)

# Write to new file.
outputPdfPath = str( 
    Path.home()
    / "Device Labels - Filled.pdf"
)
with Path(outputPdfPath).open(mode="wb") as outputStream:
    outputPdf.write(outputStream)
    outputStream.close()

print("done")
