class WordNotFoundException(Exception):
    def __init__(self, word):
        return super(
            WordNotFoundException,
            self).__init__("Cannot find {} in the dictionary!".format(word))


def get_random_word(words_api, min_length):
    word = None
    while word is None:
        response = words_api.getRandomWord(
            hasDictionaryDef=True,
            minLength=min_length)
        word = response.word
    return word


def get_word_definition(word, word_api):
    dictionary_entry = word_api.getDefinitions(
        word,
        sourceDictionaries="all",
        limit=1)

    if not dictionary_entry:
        raise WordNotFoundException(word)
    first_definition = dictionary_entry[0].text

    related_searcher = re.compile("(Plural form of |"
                                  "Of or relating to |"
                                  "Of or pertaining to the |"
                                  "Resembling a )(\w+([a-zA-Z-]+)?).")
    related_search_result = related_searcher.match(first_definition)
    if related_search_result:
        related_form = related_search_result.group(2)
        related_dictionary_entry = word_api.getDefinitions(
            related_form,
            sourceDictionaries="all",
            limit=1)
        if not related_dictionary_entry:
            return first_definition
        related_definition = related_dictionary_entry[0].text
        print (u"Your word was {}. Fetching definition "
               "of related word {}:".format(word,
                                            related_form))
        return (u"\nDefinition of {0}: {1} \n"
                "Definition of related word, {2}: {3}".format(word,
                    first_definition,
                    related_form,
                    related_definition))
    return first_definition


def run():
    random_word = get_random_word(words_api, 8)
    random_word_definition = get_word_definition(random_word, word_api)
    print u"\nYour random word is: {}".format(random_word)
    print u"Definition: {}".format(random_word_definition)


if __name__ == "__main__":
    import os
    import re
    import sys
    from wordnik import swagger, WordApi, WordsApi
    print "Welcome to Baldersash!"

    apiUrl = "http://api.wordnik.com/v4"
    # Don't normally check your credentials into version control!
    # This API key is not particularly sensitive, so do as I say not
    # as I do.
    apiKey = os.getenv("WORDNIK_API_KEY",
                       "a640d86be77d652da540e00c27b087c2cdbeee53ffd3b3457")
    client = swagger.ApiClient(apiKey, apiUrl)
    words_api = WordsApi.WordsApi(client)
    word_api = WordApi.WordApi(client)

    run()
    while True:
        prompt_message = "\nPress n to get another word or q to quit: "
        command = raw_input(prompt_message)
        if command == "q":
            sys.exit(0)
        elif command == "n":
            run()
        else:
            command = raw_input(prompt_message)
