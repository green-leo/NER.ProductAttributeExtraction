import pandas as pd

# Definition of the features extraction
# CONSTANTS WE USE
TUPLE_ID = 0
TUPLE_TAGGED_ID = 1
TUPLE_WORD_LIST = 2
TUPLE_TAG_LIST = 3


class FeatureExtractor:
    def __init__(self, name):
        self.name = name
        
    # sentense tuple is the result of process_tuple
    # we extract features from tuple and return feature value in format
    # (true/false, FeatureName, FeatureValue)
    def extract(self, word_id, sentense_tupe, addition_mode):
        pass
    
    # Return list of features supported by current features extractor
    def features_list(self):
        return [self.name]

# Check if Hypen is inside
class FE_HyphenInside(FeatureExtractor):
    def __init__(self):
        super(FE_HyphenInside, self).__init__('HyphenInside')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        return (True, self.name, '-' in word)


# Check if Hypen is inside
class FE_IsNumber(FeatureExtractor):
    def __init__(self):
        super(FE_IsNumber, self).__init__('IsNumber')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        return (True, self.name, word.isdigit())

# Check started with dollar decimal/ended with dollar
class FE_StartedDollar(FeatureExtractor):
    def __init__(self):
        super(FE_StartedDollar, self).__init__('StartedDollar')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        dollar =  len(word) > 0 and '$' == word[0] 
        return (True, self.name, dollar)


# Check started digit
class FE_StartedDigit(FeatureExtractor):
    def __init__(self):
        super(FE_StartedDigit, self).__init__('StartedDigit')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        digit =  len(word) > 0 and '9' >= word[0] and '0' <= word[0] 
        return (True, self.name, digit)

# Check end digit
class FE_EndDigit(FeatureExtractor):
    def __init__(self):
        super(FE_EndDigit, self).__init__('EndDigit')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        ll = len(word)
        digit =  ll > 0 and '9' >= word[ll-1] and '0' <= word[ll-1] 
        return (True, self.name, digit)


# True if no letters included
class FE_DoesNotHaveLetters(FeatureExtractor):
    def __init__(self):
        super(FE_DoesNotHaveLetters, self).__init__('NoLetters')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        for c in word:
            if c >= 'a' and c <= 'z':
                return (True, self.name, False)
            if c >= 'A' and c <= 'Z':
                return (True, self.name, False)
            
        return (True, self.name, True)


# Word position
class FE_WordPos(FeatureExtractor):
    def __init__(self):
        super(FE_WordPos, self).__init__('WordPosition')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        return (True, self.name, word_id)


# and before
class FE_And_Pos_M1(FeatureExtractor):
    def __init__(self):
        super(FE_And_Pos_M1, self).__init__('And_Pos_M1')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        andBefore = False
        if word_id > 0:
            word = sentense_tupe[TUPLE_WORD_LIST][word_id - 1]
            andBefore = ('and' == word)                        
        return (True, self.name, andBefore)

# and after
class FE_And_Pos_P1(FeatureExtractor):
    def __init__(self):
        super(FE_And_Pos_P1, self).__init__('And_Pos_P1')
        
    def extract(self, word_id, sentense_tupe, addition_mode):
        andAfter = False
        if word_id + 1< len(sentense_tupe[TUPLE_WORD_LIST]):
            word = sentense_tupe[TUPLE_WORD_LIST][word_id + 1]
            andAfter = ('and' == word)                        
        return (True, self.name, andAfter)


# Represent the current word itself
class FE_W0(FeatureExtractor):
    def __init__(self):
        super(FE_W0, self).__init__('W0_')
        self.word2index = {}
        self.current_index = int(0)

    def extract(self, word_id, sentense_tupe, addition_mode):
        word = sentense_tupe[TUPLE_WORD_LIST][word_id]
        if word not in self.word2index.keys():
            if not addition_mode:
                return (False, self.name, 0)
            self.word2index[word] = self.current_index
            self.current_index = int(self.current_index + 1)
        return (True, self.name+str(self.word2index[word]), 1)
    
    def features_list(self):
        return [self.name + str(i) for i in range(self.current_index)]
    


# Class which contains feature extractors we would like to apply
class FeatureExtractionContainer:
    def __init__(self):
        self.feature_extractors = [FE_HyphenInside(), FE_IsNumber(), 
                                   FE_W0(), FE_StartedDollar(), FE_DoesNotHaveLetters(),
                                   FE_StartedDigit(), FE_EndDigit(), FE_WordPos(),
                                   FE_And_Pos_M1(), FE_And_Pos_P1()]

    # This is extraction from one specific tuple
    def extract_from_tuple(self, word_id, sentense_tuple, addition_mode):
        features = {}
        for fe in self.feature_extractors:
            fe_result = fe.extract(word_id, sentense_tuple, addition_mode)
            if fe_result[0]:
                features[fe_result[1]] = fe_result[2]
        return features
    
    # result is a list of tuples which will include
    # word_features_list := (tuple_id, IS_TAGGED, word, word_id, tag, features)
    def process_sentense(self, sentense_tuple, addition_mode):
        result = []
        tuple_id = sentense_tuple[TUPLE_ID]
        tagged = sentense_tuple[TUPLE_TAGGED_ID]
        
        
        for word_id in range(len(sentense_tuple[TUPLE_WORD_LIST])):
            features = self.extract_from_tuple(word_id, sentense_tuple, addition_mode)
            tag = sentense_tuple[TUPLE_TAG_LIST][word_id]
            result.append( (tuple_id, tagged, sentense_tuple[TUPLE_WORD_LIST][word_id], word_id, tag, features) )
            
        return result

    # result is a list of tuples which will include
    # word_features_list := (tuple_id, IS_TAGGED, word, word_id, tag, features)
    def process_sentenses(self, sentense_tuples, addition_mode=True):
        result = []
        for sentense in sentense_tuples:
            result = result + self.process_sentense(sentense, addition_mode)
            
        return result
        
    # This function takes list of tuples produced by
    # process_sentense and put it in nice pandas.DataFrame
    def features_pandalizer(self, word_features_list):
        features_vector = {}
        features_vector['TupleID'] = []
        features_vector['Tagged'] = []
        features_vector['Tag'] = []
        features_vector['word'] = []
        features_vector['WordID'] = []
        
        # Inject features
        for fe in self.feature_extractors:
            for fname in fe.features_list():
                features_vector[fname] = []
        
        # Phase of creating long lists
        for word_features in word_features_list:
            features_vector['TupleID'].append(word_features[0])
            features_vector['Tagged'].append(word_features[1])
            features_vector['Tag'].append(word_features[4])
            features_vector['word'].append(word_features[2])
            features_vector['WordID'].append(word_features[3])
            
            # working with features
            for fe in self.feature_extractors:
                for fname in fe.features_list():
                    if fname in word_features[5].keys():
                        #print('FName=', fname, ' Value=', word_features[5][fname])
                        features_vector[fname].append(int(word_features[5][fname]))
                    else:
                        features_vector[fname].append( 0)
                        
            #print(features_vector)
                        
        df = pd.DataFrame(features_vector)
        return df
    
