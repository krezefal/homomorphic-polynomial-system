import unittest
import random
import time
import timeit
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

from homomorphic_polynomial_system.keygen import generate_abramov_keypair


class TestAsymptotic(unittest.TestCase):
    reference_base = 7
    reference_degree = 8

    @classmethod
    def setUpClass(cls):  # Keypair will be generated once for all these test cases
        cls.private_key, cls.public_key = \
            generate_abramov_keypair(cls.reference_base, cls.reference_degree)

    def test_encryption_time(self):
        number_lengths = np.arange(0, 19)
        times = []

        for number_length in number_lengths:
            number_to_encrypt = 10 ** number_length
            time_arr = timeit.repeat(lambda: self.public_key.encrypt(number_to_encrypt), number=1, repeat=10)
            avg_time = mean(time_arr)
            times.append(avg_time)

        plt.figure()
        plt.plot(number_lengths, times)
        plt.grid()
        plt.xticks(number_lengths)
        plt.ylabel('Elapsed time')
        plt.xlabel('Digit number')
        plt.title("Measured encryption time")
        plt.savefig("plots/encryption_time.png")

    def test_addition_time(self):
        number_of_operations = 1000
        times = []
        enc_times = []

        i = 1
        while i <= number_of_operations:

            sum_ = random.randint(10, 100)

            j = 1
            total_time = 0
            while j <= i:
                rand_number = random.randint(10, 100)
                start = time.time()
                sum_ += rand_number
                end = time.time()
                iteration_time = end - start
                total_time += iteration_time
                j += 1

            sum_ = random.randint(10, 100)
            encrypted_sum = self.public_key.encrypt(sum_)

            j = 1
            enc_total_time = 0
            while j <= i:
                rand_number = random.randint(10, 100)
                encrypted_rand_number = self.public_key.encrypt(rand_number)
                start = time.time()
                encrypted_sum += encrypted_rand_number
                end = time.time()
                iteration_time = end - start
                enc_total_time += iteration_time
                j += 1

            times.append(total_time)
            enc_times.append(enc_total_time)

            i += 1

        plt.figure()
        plt.plot(np.arange(1, number_of_operations + 1), times)
        plt.plot(np.arange(1, number_of_operations + 1), enc_times)
        plt.grid()
        plt.ylabel('Elapsed time')
        plt.xlabel('Number of operations')
        plt.title("Average addition time")
        plt.savefig("plots/addition_time.png")

    def test_multiplication_time(self):
        number_of_operations = 1000
        times = []
        enc_times = []

        i = 1
        while i <= number_of_operations:

            sum_ = random.randint(10, 100)

            j = 1
            total_time = 0
            while j <= i:
                rand_number = random.randint(10, 100)
                start = time.time()
                sum_ *= rand_number
                end = time.time()
                iteration_time = end - start
                total_time += iteration_time
                j += 1

            sum_ = random.randint(10, 100)
            encrypted_sum = self.public_key.encrypt(sum_)

            j = 1
            enc_total_time = 0
            while j <= i:
                rand_number = random.randint(10, 100)
                encrypted_rand_number = self.public_key.encrypt(rand_number)
                start = time.time()
                encrypted_sum *= encrypted_rand_number
                end = time.time()
                iteration_time = end - start
                enc_total_time += iteration_time
                j += 1

            times.append(total_time)
            enc_times.append(enc_total_time)

            i += 1

        plt.figure()
        plt.plot(np.arange(1, number_of_operations + 1), times)
        plt.plot(np.arange(1, number_of_operations + 1), enc_times)
        plt.grid()
        plt.ylabel('Elapsed time')
        plt.xlabel('Number of operations')
        plt.title("Average multiplication time")
        plt.savefig("plots/multiplication_time.png")


if __name__ == '__main__':
    unittest.main(verbosity=2)
