import timeit
items = [str(i) for i in range(100000)]
as_list = items
as_dict = {item: True for item in items}
list_time = timeit.timeit(lambda: '99999' in as_list, number=100)
dict_time = timeit.timeit(lambda: '99999' in as_dict, number=100)
print(f'list scan: {list_time:.6f} seconds for 100 lookups')
print(f'dict     : {dict_time:.6f} seconds for 100 lookups')