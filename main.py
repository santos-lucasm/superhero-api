import requests
import pdf_handler

def request_superheros():
    """
    @description Returns first 10 superheros found in the API
    @return Array containing first 10 superheros
    """

    print("Sending HTTP request...")
    api_url = "https://akabab.github.io/superhero-api/api/"
    response = requests.get(api_url + "all.json")

    if response.status_code == 200:
        return response.json()[0:10]
    else:
        print("Error requesting API")


def ordenate_superheros(array):
    """
    @description Group received array of heros by hero occupation
    @param array Array containing heros to be sorted
    @return Dictionary sorted by occupation
    """

    print("Grouping heros by occupation...")
    ret = {} # Init empty dictionary

    for hero in array:
        # hero_id will be used as the dict value
        hero_id = hero["id"]

        # occupations will be split to be used as dict keys
        occupations = hero['work']['occupation']

        # Some heros use ";" instead of "," to enumerate its occupations
        occupations = occupations.replace(";", ",")
        occupations = occupations.split(', ')

        for occupation in occupations:
            if occupation not in ret: # Add key pair to the dict
                ret.__setitem__(occupation, [hero_id])
            else: # Heros with the same occupation should have its id append to the value
                current_ids = ret.get(occupation)
                current_ids.append(hero_id)
                ret.__setitem__(occupation, current_ids)

    return ret


def add_hero_info_to_output(pdf, hero):
    """
    @description Add hero info to the pdf output
    @param pdf PDF instance in which the data will be stored
    @param hero Hero object received from API that contains its briography data
    """

    text = 'Full Name: ' + hero['biography']['fullName']
    pdf.add_text(text)

    text = 'Alter Egos: ' + hero['biography']['alterEgos']
    pdf.add_text(text)

    text = 'Aliases:'
    for alias in hero['biography']['aliases']:
        text += ' ' + alias
    pdf.add_text(text)

    text = 'Place of Birth Picture of the hero: ' + hero['biography']['placeOfBirth']
    pdf.add_text(text)

    pdf.jump_line()


def generate_output_file(heros, occupations):
    """
    @brief Generates a pdf file containing all the different hero occupations and
        list all the heros corresponding to each occupation
    @param heros Hero array that contains its data
    @param occupations Dictionary relating a hero occupation to its biography data
    """
    # Initialize pdf outputs
    pdf_doc = pdf_handler.PDF()

    # Add the main title
    pdf_doc.add_title("SUPERHERO ACQUIRED DATA")

    # For each occupation in dictionary
    for key in occupations:
        # Add the section title (which is the occupation)
        pdf_doc.add_section_title(key)

        # Add the heros listed in this occupation
        for hero_id in occupations.get(key):
            # A hero will be listed for every occupation it has
            [ (add_hero_info_to_output(pdf_doc, hero)) for hero in heros if(hero['id'] == hero_id) ]

    # Generate PDF output  
    pdf_doc.generate_output("output.pdf")

if __name__ == "__main__":
    """
    @brief
        Main application shall request 10 first superheros from an API
        Group superheros by their common occupation
        For each superhero, list some of its biography info
        Generate a pdf with the filtered data
    """
    # Get heros from API
    heros = request_superheros()
    # Init a dictionary of { occupation: [hero_ids] }

    occupations = ordenate_superheros(heros)

    generate_output_file(heros, occupations)
    
