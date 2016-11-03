# -*- coding: utf-8 -*-
import re

_BID = ':'  # заявка (запрос полной информации по заданному объекту, определяемому префиксом)

_RE_PREFIX = re.compile('^[A-Za-z]$')  # префикс: 1 латинский символ
_RE_NAME = re.compile('^[A-Za-z]+$')  # имя: латинские символы
_RE_VALUE = re.compile('^[A-Za-zА-Яа-я0-9 ]*$')  # значение
_RE_PREFIX_NAME_WODS = re.compile('[A-Za-z]\.[A-Za-z]+')  # префикс.имя
_RE_PREFIX_NAME = re.compile('\$[A-Za-z]\.[A-Za-z]+')  # $префикс.имя


class Triplet:
    """
    ТРИПЛЕТ
    Принимает:
        prefix (str) - префикс (1 латинский символ)
        name (str) - имя параметра (латинские символы)
        value - значение параметра
    """
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if not isinstance(value, (str, int, float, Triplet, TriplexString)):
            raise ValueError('Значение должно быть строкой, числом, триплетом или триплексной строкой')
        if re.match(_RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(_RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')
        # TODO может быть и не строкой (следует уточнить)
        if isinstance(value, str) and value != _BID and re.match(_RE_VALUE, value) is None:
            raise ValueError

        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '${}.{}='.format(self.prefix, self.name)
        if self.value == _BID:
            _ += _BID
        elif isinstance(self.value, str):
            _ += '\'{}\''.format(self.value)
        else:
            _ += str(self.value)
        _ += ';'
        return _

    def __add__(self, other):
        if isinstance(other, Triplet):
            return TriplexString(self, other)
        if isinstance(other, TriplexString):
            return TriplexString(self, *other)
        else:
            raise ValueError

    def __eq__(self, other):
        return isinstance(other, Triplet) and \
               self.name == other.name and \
               self.prefix == other.prefix and \
               self.value == other.value


class TriplexString:
    """
    ТРИПЛЕКСНАЯ СТРОКА
    Принимает:
        *triplets (Triplet) - триплеты
    """
    def __init__(self, *triplets):
        for _ in triplets:  # CHECK проверить скорость работы через filter
            if not isinstance(_, Triplet):
                raise ValueError('Аргументы должны быть триплетами')
        self.triplets = list(triplets)

        # удаление повторов триплетов (по префиксам и именам)
        for trp in self.triplets.copy():
            # триплеты с данными префиксами и именами
            triplets_to_remove = [_trp for _trp in self.triplets if trp.prefix == _trp.prefix and trp.name == _trp.name]
            triplets_to_remove = triplets_to_remove[:-1]  # исключение последнего найденного триплета
            for rem_trp in triplets_to_remove:
                self.triplets.remove(rem_trp)

    def __len__(self):
        return len(self.triplets)

    def __add__(self, other):
        if isinstance(other, Triplet):
            return TriplexString(*(self.triplets + [other]))
        elif isinstance(other, TriplexString):
            return TriplexString(*(self.triplets + other.triplets))
        else:
            raise ValueError('Должен быть триплет или триплексная строка')

    def __str__(self):
        return ''.join(tuple(str(trp) for trp in self.triplets))

    def __contains__(self, item):
        # TODO возможно, стоит включить возможность проверки включения по префиксу и имени
        if not isinstance(item, Triplet):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == item.prefix and \
               trp.name == item.name and \
               trp.value == item.value:
                return True
        return False

    def __getitem__(self, key):
        # TODO CHECK
        if isinstance(key, str):  # элемент по ключу
            if re.match(_RE_PREFIX, key) is not None:  # получить триплеты по префиксу в виде триплесной строки
                return TriplexString(*[trp for trp in self.triplets if trp.prefix == key])
            elif re.match(_RE_PREFIX_NAME_WODS, key) is not None:  # получить значение по префиксу и имени
                key = key.upper().split('.')
                for trp in self.triplets:
                    if trp.prefix == key[0] and trp.name == key[1]:
                        return trp.value
                return None
            else:
                raise ValueError('Неверный формат данных')
        else:  # элемент по индексу
            return self.triplets[key]

    def __eq__(self, other):
        # CHECK возможно, стоит замерить скорость работы
        if not isinstance(other, TriplexString):
            raise ValueError

        if len(self.triplets) != len(other):
            return False
        for triplet in other:
            if triplet not in self.triplets:
                return False
        return True

    def __iter__(self):
        return iter(self.triplets)

    def add(self, other):
        """
        СЛОЖЕНИЕ ТРИПЛЕКСНОЙ СТРОКИ С ТРИПЛЕКСНОЙ СТРОКОЙ ИЛИ ТРИПЛЕТОМ
        Эквивалентно сложению через оператор "+"
        Принимает:
            other (TriplexString или Triplet) - триплексная строка или триплет
        Возвращает:
            (TriplexString)
        """
        return self.__add__(other)

    def del_trp(self, prefix, name):
        # CHECK
        """
        УДАЛИТЬ ТРИПЛЕТ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс (1 латинский символ)
            name (str) - имя параметра (латинские символы)
        Вызывает исключение ValueError, если триплет не найден
        """
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if re.match(_RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(_RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')

        for trp in self.triplets:
            if trp.prefix == prefix and trp.name == name:
                self.triplets.remove(trp)
                return
        raise ValueError('Триплет не найден')

    def del_trp_pref(self, prefix):
        # CHECK
        """
        УДАЛИТЬ ВСЕ ТРИПЛЕТЫ С ЗАДАННЫМ ПРЕФИКСОМ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс
        """
        if not isinstance(prefix, str):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == prefix:
                self.triplets.remove(trp)