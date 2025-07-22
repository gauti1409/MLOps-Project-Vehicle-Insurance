import sys
import logging

"""
NOTES TO UNDERSTAND THE FUNCTION : error_message_detail

1. _, _, exc_tb = error_detail.exc_info()

    - error_detail.exc_info() (which is sys.exc_info() when error_detail is sys) returns a tuple containing information about the exception 
      that is currently being handled:

    - type: The exception type (e.g., ValueError).

    - value: The exception instance (the error object itself).

    - traceback: A traceback object, which contains the call stack information leading up to the exception.

- The _ (underscore) is used as a placeholder for the type and value elements because the function only needs the traceback object (exc_tb) 
  for extracting file and line number details.


2. file_name = exc_tb.tb_frame.f_code.co_filename

    - exc_tb: The traceback object.

    - tb_frame: The frame object at the current level of the traceback. A frame object represents a stack frame in the Python execution model.

    - f_code: The code object being executed in that frame. A code object contains immutable properties of the code, including its name, 
      arguments, and filename.

    - co_filename: The name of the file in which the code object was compiled. This gives you the file where the error originated.

3.  line_number = exc_tb.tb_lineno

    - tb_lineno: The line number in the code where the exception occurred within that specific frame.

"""

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.

    1. error: Exception: This parameter is expected to be the exception object itself that was caught 
    (e.g., ValueError, TypeError, or a custom exception).

    2. error_detail: sys: This parameter is expected to be the sys module. The sys module provides access to system-specific parameters and 
    functions, including information about the current exception.

    3. -> str: This is a type hint indicating that the function is expected to return a string.
    """
    # Extract traceback details (exception information) - This needs to be called when an exception is active
    _, _, exc_tb = error_detail.exc_info()
    
    # file_name = exc_tb.tb_frame.f_code.co_filename
    # line_number = exc_tb.tb_lineno

    # Handle cases where exc_tb might be None if no exception is currently handled
    if exc_tb is None:
        file_name = "<unknown_file>"
        line_number = "<unknown_line>"
    else:
        # Get the file name where the exception occurred
        file_name = exc_tb.tb_frame.f_code.co_filename

        # Create a formatted error message string with file name, line number, and the actual error
        line_number = exc_tb.tb_lineno

    error_message = f"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}"
    
    # Log the error for better tracking
    logging.error(error_message)
    
    return error_message

class MyException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes the USvisaException with a detailed error message.

        :param error_message: A string describing the error.
        :param error_detail: The sys module to access traceback details.
        """
        # Call the base class constructor with the error message
        super().__init__(error_message)

        # Format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.error_message