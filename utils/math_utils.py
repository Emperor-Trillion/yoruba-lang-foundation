def mean(num: list[float]) -> float:
    """Calculates the mean of a list of number

    Args:
        num (list[float]): a list of float numbers

    Returns:
        float: Average of the list of numbers
    """
    if all(isinstance(each, float) for each in num):
        return sum(num) / len(num) 

    else:
        raise TypeError(f"Expecting all values to be of type float")
