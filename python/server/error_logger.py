import sys

class ErrorLogger:

  warning_output = sys.stderr
  error_output = sys.stderr

  @classmethod
  def warning(self, text):
    print >> self.warning_output, "WARNING:", text

  @classmethod
  def error(self, text):
    print >> self.error_output, "ERROR:", text

    
    
