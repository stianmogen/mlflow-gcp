from etl import run_etl


def main(request=None):
    """
    This is the entry point for Google Cloud Functions.
    It receives an HTTP request and triggers the ETL process.
    """
    try:
        run_etl()
        return 'ETL process completed successfully', 200
    except Exception as e:
        return f'ETL failed: {str(e)}', 500
