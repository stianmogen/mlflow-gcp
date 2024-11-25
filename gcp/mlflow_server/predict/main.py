from predict import run_predict


def main(request=None):
    """
    This is the entry point for Google Cloud Functions.
    It receives an HTTP request and triggers the prediction process.
    """
    try:
        run_predict()
        return 'Prediction process completed successfully', 200
    except Exception as e:
        return f'Prediction process failed: {str(e)}', 500
