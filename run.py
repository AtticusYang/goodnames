import csv

def load_lastname(filename):
    lastname_set = set()
    with open(filename, 'r') as fd:
        for line in fd.readlines():
          line = line.strip()
          lastname_set.add(line)

    return lastname_set

def load_names_with_gender(filenames):
    items = []
    for filename in filenames:
        with open(filename, 'r') as fd:
            for line in fd.readlines()[1:]:
                line = line.strip()
                pieces = line.split(',')
                items.append(pieces)

    return items

def get_3names(name, lastname_set):
    '''
    last_name，姓;middle_name,辈份;first_name,最后一个字
    '''
    if len(name) >= 5:
        return
    # 复姓
    if name[0:2] in lastname_set:
        if len(name) == 2:
            return

        last_name = name[0:2]
        middle_name = '' if len(name) == 3 else name[2]
        first_name = name[-1]
    elif name[0] in lastname_set:
        last_name = name[0]
        middle_name = '' if len(name) == 2 else name[1]
        first_name = name[-1]
    else:
        return

    return last_name, middle_name, first_name


if __name__ == '__main__':
    lastname_file = 'data/百家姓.txt'
    lastname_set = load_lastname(lastname_file)

    names_file = "data/Ancient_Names_Simple_Gender.txt"
    items = load_names_with_gender([names_file])

    word_invert_index = {}
    word_name_dict = {}

    for item in items:
      name, gender = item[0], item[1]
      ans = get_3names(name, lastname_set)
      if not ans:
          continue

      last_name, middle_name, first_name = ans

      if middle_name == '':
          if first_name not in word_invert_index.keys():
              word_invert_index[first_name] = set([first_name])
          else:
              word_invert_index[first_name].add(first_name)

          if first_name not in word_name_dict.keys():
              word_name_dict[first_name] = [name]
          else:
              word_name_dict[first_name].append(name)
      else:
          t = ''.join([middle_name, first_name])
          if first_name not in word_invert_index.keys():
              word_invert_index[first_name] = set([t])
          else:
              word_invert_index[first_name].add(t)

          if middle_name not in word_invert_index.keys():
              word_invert_index[middle_name] = set([t])
          else:
              word_invert_index[middle_name].add(t)

          if t not in word_name_dict.keys():
              word_name_dict[t] = [name]
          else:
              word_name_dict[t].append(name)

    for word in sorted(word_invert_index, key=lambda k: len(word_invert_index[k]), reverse=True):
        #print('{},{},{}'.format(word, len(word_invert_index[word]), \
        #  '|'.join(word_invert_index[word])))

        tmp_dict = {}
        for x in word_invert_index[word]:
            #print('{},{},{}'.format(x, len(word_name_dict[x]),\
            # '|'.join(word_name_dict[x])))
             tmp_dict[x] = word_name_dict[x]
        sorted_tmp_dict = sorted(tmp_dict, key = lambda k: len(tmp_dict[k]), reverse=True)
        print('{},{},{}'.format(word, len(word_invert_index[word]), \
          '|'.join(sorted_tmp_dict)))

        for x in sorted_tmp_dict:
          print('{},{},{}'.format(x, len(word_name_dict[x]),\
            '|'.join(word_name_dict[x])))  
