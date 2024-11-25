from pre_process import run_pre_process


def main(request=None):
    """
    This is the entry point for Google Cloud Functions.
    It receives an HTTP request and triggers the pre-processing.
    """
    try:
        run_pre_process()
        return 'Pre-process completed successfully', 200
    except Exception as e:
        return f'Pre-process failed: {str(e)}', 500


if __name__ == '__main__':
    main()
