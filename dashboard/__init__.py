import sys
from dashboard import views

# Backward compatibility alias
sys.modules['dashboard.pages'] = views
