from functools import partial
import numpy


random = partial(numpy.random.uniform, low=-1, high=1)


class FFANN(object):
    '''
    network = FFANN(config, function)

    where config is a list containint how many neurons exist in each layer:
    config = [2, 3] -> two layers; two neurons in the first one and three in the
    second.
    '''

    def __init__(self, config, function, fill_with=random):
        self.f = function

        # take the config and pair its elements to create the shapes for the
        # different layers. add one to the first dimension to accomodate for the
        # bias weights. add one to the second dimension to accomodate for the
        # bias input for the next layer.
        self.shapes = [config[i:i + 2] for i in range(len(config) - 1)]
        self.layers = [fill_with(size=(i + 1, j + 1)) for i, j in self.shapes[:-1]]

        i, j = self.shapes[-1]
        self.layers.append(fill_with(size=(i + 1, j)))

        self.elements = numpy.cumsum([(i + 1) * j for i, j in self.shapes])

    def eval(self, input):
        # include the bias.
        input = self.f(numpy.append(input, 1))

        output = numpy.dot(input, self.layers[0])
        for layer in self.layers[1:]:
            output = self.f(numpy.dot(output, layer))

        return output

    def __str__(self):
        layers = [layer[:, :m] for (_, m), layer in zip(self.shapes, self.layers)]
        return str(numpy.array(layers))


class EvolvableFFANN(FFANN):
    def __init__(self, config, function, fill_with=random):
        self.fitness = 0
        super(self.__class__, self).__init__(config, function, fill_with)

    def _getpos(self, key):
        if key >= self.elements[-1]:
            raise IndexError("list index out of range")

        if key < 0:
            key = self.elements[-1] + key

        i = j = 0
        for num_elements in self.elements:
            if key >= num_elements:
                i += 1
                j += num_elements
            else:
                break

        n, m = self.shapes[i]
        x = (key - j) // m
        y = (key - j) % m

        return i, x, y, n, m

    def __getitem__(self, key):
        i, x, y, n, m = self._getpos(key)
        return self.layers[i][:, :m][x, y]

    def __setitem__(self, key, value):
        i, x, y, n, m = self._getpos(key)
        self.layers[i][:, :m][x, y] = value

    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)

    def __len__(self):
        return self.elements[-1]
