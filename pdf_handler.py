from fpdf import FPDF

class PDF:

    def __init__(self):
        """
        @brief Initializes FPDF instance
        """
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size = 12)

    def add_title(self, title):
        """
        @brief Add a new title w/ white bg color and border
        @param title Name of the title
        """
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.cell(0, 6, title, 1, 1, 'C', 1)
        self.jump_line()

    def add_section_title(self, title):
        """
        @brief Add a new title w/ blue bg color to the output
        @param title Name of the title
        """
        self.pdf.set_fill_color(195, 176, 145)
        self.pdf.cell(0, 6, title, 0, 1, 'L', 1)
        self.jump_line()

    def add_text(self, text):
        """
        @brief Add text w/ white bg color to the output
        @param text Text to be added
        """
        self.pdf.set_fill_color(255, 248, 227)
        self.pdf.cell(0, 6, text, 0, 1, 'L', 1)

    def jump_line(self):
        """
        @brief Add a blank line to the pdf w/ white bg
        """
        self.pdf.ln(4)

    def generate_output(self, fileName):
        """
        @brief Generates a pdf file with previously added data
        @param fileName Name of the file to be saved
        """
        self.pdf.output(fileName)