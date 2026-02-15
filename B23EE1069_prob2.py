import sys
from collections import defaultdict

class SimpleTokenizer:
    def __init__(self):
        self.corpus = []
        self.vocab = []

    def init_vocab(self, strings):
        for sentence in strings.split('.'):
            for word in sentence.split():
                self.corpus.append(list(word) + ['</s>'])

    def get_pair_freq(self):
        freq = defaultdict(int)

        for word in self.corpus:
            for i in range(len(word) - 1):
                freq[(word[i], word[i + 1])] += 1

        return freq
    
    def merge_pair(self, t_l, t_r):
        t_new = t_l + t_r

        for i, word in enumerate(self.corpus):
            j = 0
            new_word = []

            while j < len(word):
                if j < len(word) - 1 and word[j] == t_l and word[j + 1] == t_r:
                    new_word.append(t_new)
                    j += 2
                else:
                    new_word.append(word[j])
                    j += 1

            self.corpus[i] = new_word

    def train(self, k):
        for _ in range(k):
            freq = self.get_pair_freq()
            if not freq: break

            best = max(freq, key=freq.get)
            self.vocab.append(best)

            self.merge_pair(*best)

    def tokenize(self, text):
        tokens = []

        for word in text.split():
            symbols = list(word) + ['</s>']

            for t_l, t_r in self.vocab:
                j = 0
                new_sym = []

                while j < len(symbols):
                    if j < len(symbols) - 1 and symbols[j] == t_l and symbols[j + 1] == t_r:
                        new_sym.append(t_l + t_r)
                        j += 2
                    else:
                        new_sym.append(symbols[j])
                        j += 1
                
                symbols = new_sym

            tokens.extend(symbols)

        return tokens


def example():
    tokenizer = SimpleTokenizer()

    vocab = "I want a banana. I like it very much. Bananas are eaten by monkeys."
    tokenizer.init_vocab(vocab)
    tokenizer.train(50)

    print("Vocab\n")
    print(tokenizer.vocab)
    print()
    print("Merged Vocab\n")
    print(tokenizer.tokenize("I like monkeys."))


if __name__ == "__main__":
    filename = sys.argv[2]
    k = sys.argv[1]
    k = (int)(k)

    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    tokenizer = SimpleTokenizer()

    tokenizer.init_vocab(text)
    tokenizer.train(k)

    tokens = tokenizer.tokenize(text)

    print("Tokens:")
    print(tokens)