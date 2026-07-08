import random
from sort import my_sort

def test_random():
    for _ in range(1000):
        length = random.randint(0, 50)
        lst = [random.randint(-1000, 1000) for _ in range(length)]
        sorted_lst = my_sort(lst)
        # check sorted
        assert all(sorted_lst[i] <= sorted_lst[i+1] for i in range(len(sorted_lst)-1))
        # check multiset equality
        assert sorted(sorted_lst) == sorted(lst)
    print("Random tests passed")

if __name__ == "__main__":
    test_random()
