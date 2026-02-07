import random
from collections import defaultdict


def tokenize(text):
    return text.split()

class SentimentDataset:
    def __init__(self, pos_file="pos.txt", neg_file="neg.txt"):
        self.data = []

        # adding positive sentences
        with open(pos_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower() # removing whitespaces and making it lowercase
                if line:
                    self.data.append((line, 1))

        # adding negative sentences
        with open(neg_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower() # removing whitespaces and making it lowercase
                if line:
                    self.data.append((line, 0)) 

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text, label = self.data[idx]
        tokens = tokenize(text)

        return {
            "text": text,
            "X": tokens,
            "y": label
        }
    
def train_test_split(dataset, test_ratio=0.2, seed=42):
    random.seed(seed)

    data = dataset.data.copy()
    random.shuffle(data)

    split = int(len(data) * (1 - test_ratio))

    train_data = data[:split]
    test_data = data[split:]

    train_set = SentimentDataset.__new__(SentimentDataset)
    test_set = SentimentDataset.__new__(SentimentDataset)

    train_set.data = train_data
    test_set.data = test_data

    return train_set, test_set


class NaiveBayes:
    def __init__(self, alpha=1):
        self.vocab = set()
        self.alpha = alpha
        
        self.wordCnt_pos = defaultdict(int)
        self.wordCnt_neg = defaultdict(int)

        self.pos_tokens = 0
        self.neg_tokens = 0

        self.pos_egs = 0
        self.neg_egs = 0

    def train(self, dataset):
        for item in dataset:
            tokens = item["X"]
            label = item["y"]

            self.vocab.update(tokens)

            if label == 1:
                self.pos_egs += 1
                for t in tokens:
                    self.wordCnt_pos[t] += 1
                    self.pos_tokens += 1

            else:
                self.neg_egs += 1
                for t in tokens:
                    self.wordCnt_neg[t] += 1
                    self.neg_tokens += 1

        self.K = len(self.vocab)

    def calc_prior_prob(self):
        pos_prob = self.pos_egs / (self.pos_egs + self.neg_egs)
        neg_prob = self.neg_egs / (self.pos_egs + self.neg_egs)

        return pos_prob, neg_prob
    
    def predict(self, tokens):
        p_pos, p_neg = self.calc_prior_prob()

        for t in tokens:
            p_cond_pos = (self.wordCnt_pos[t] + self.alpha) / (self.pos_tokens + self.alpha * self.K)
            p_cond_neg = (self.wordCnt_neg[t] + self.alpha) / (self.neg_tokens + self.alpha * self.K)

            p_pos *= p_cond_pos
            p_neg *= p_cond_neg

        return 1 if p_pos > p_neg else 0
    
    def evaluate(self, dataset):
        correct = 0

        for item in dataset:
            if self.predict(item["X"]) == item["y"]: correct += 1

        return correct / len(dataset)
    
def example():
    dataset = SentimentDataset("pos.txt", "neg.txt")

    train_data, test_data = train_test_split(dataset, test_ratio=0.1)

    print("Train size:", len(train_data))
    print("Test size:", len(test_data))

    model = NaiveBayes(alpha=1)
    model.train(train_data)

    print(f"Train Accuracy: {model.evaluate(train_data)}")
    print(f"Test Accuracy: {model.evaluate(test_data)}")


if __name__ == "__main__":
    # example()
    dataset = SentimentDataset("pos.txt", "neg.txt")

    model = NaiveBayes(alpha=1)
    model.train(dataset)

    print("Enter a sentence: ")
    sentence = str(input())
    tokens = tokenize(sentence.strip().lower())

    print(model.predict(tokens))