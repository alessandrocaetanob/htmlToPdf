import azure.functions as func
import pdfkit
import logging
import os
from opencensus.ext.azure.log_exporter import AzureLogHandler

app = func.FunctionApp()

# Initialize Application Insights logging
connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
if connection_string:
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string=connection_string))
else:
    logger = logging.getLogger(__name__)
    logger.warning("Application Insights connection string not found in environment variables")

@app.function_name(name="HtmlToPdfFunction")
@app.route(route="HtmlToPdf", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def html_to_pdf(req: func.HttpRequest) -> func.HttpResponse:
    try:
        html_content = req.get_body().decode('utf-8')
        pdf = pdfkit.from_string(html_content, False, options={"enable-local-file-access": ""})
        logger.info("HTML to PDF conversion successful")
        return func.HttpResponse(pdf, mimetype='application/pdf', status_code=200)
    except Exception as e:
        logger.exception("Error converting HTML to PDF")
        return func.HttpResponse("Failed to convert HTML to PDF", status_code=500)
