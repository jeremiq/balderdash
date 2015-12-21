def get_random_word(words_api, min_length):
    response = words_api.getRandomWord(
        hasDictionaryDef=True,
        minLength=min_length)
    return response.word


def get_word_definition(word, word_api):
    first_definition = word_api.getDefinitions(
        word,
        sourceDictionaries='wiktionary',
        limit=1)[0].text
    return first_definition


def main():
    print "Welcome to Baldersash!"
    import os
    from wordnik import swagger, WordApi, WordsApi
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = os.getenv('WORDNIK_API_KEY')
    client = swagger.ApiClient(apiKey, apiUrl)
    words_api = WordsApi.WordsApi(client)
    word_api = WordApi.WordApi(client)

    random_word = get_random_word(words_api, 8)
    random_word_definition = get_word_definition(random_word, word_api)

    print "Your random word is: {}".format(random_word)
    print "Definition: {}".format(random_word_definition)


if __name__ == '__main__':
    main()
