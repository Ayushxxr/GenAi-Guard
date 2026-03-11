class SandboxExecutor:
    def __init__(self):
        # Implementation removed for external model integration
        self.model = None

    def load_local_model(self):
        pass

    def score_response(self, response_text):
        pass

    def run_tests(self, test_prompts, target_url=None):
        # Implementation removed for external model integration
        pass

    def generate_report_data(self, results):
        pass

    def generate_report(self, results):
        pass

# Keep to prevent import errors in routes.py
TEST_PROMPTS = []
