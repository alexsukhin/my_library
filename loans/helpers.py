def is_prime(number):
	validate_is_prime_input(number)
	if number <= 1:
		return False
	if number == 2:
		return True  
	largest_factor = int(number**0.5) + 1
	for factor in range(2, largest_factor):
		if number % factor == 0:
			return False
	return True

def validate_is_prime_input(input):
	if not(isinstance(input, int) and (input > 0)):
		raise ValueError("is_prime is called with argument {input}, but a positive integer was expected")