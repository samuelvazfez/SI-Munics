# vss_common.py
import random
from typing import List, Tuple

class VSSCommon:
    def __init__(self):
        self.field_prime = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001
    
    def generate_polynomial(self, secret: int, degree: int) -> List[int]:
        coefficients = [secret % self.field_prime]
        for _ in range(degree):
            coeff = random.randint(1, 1000)
            coefficients.append(coeff % self.field_prime)
        return coefficients
    
    def evaluate_polynomial(self, coefficients: List[int], x: int) -> int:
        result = 0
        for coeff in reversed(coefficients):
            result = (result * x + coeff) % self.field_prime
        return result
    
    def lagrange_interpolation(self, points: List[Tuple[int, int]], x: int = 0) -> int:
        result = 0
        for i, (xi, yi) in enumerate(points):
            numerator, denominator = 1, 1
            for j, (xj, _) in enumerate(points):
                if i != j:
                    numerator = (numerator * (x - xj)) % self.field_prime
                    denominator = (denominator * (xi - xj)) % self.field_prime
            lagrange_coeff = (numerator * pow(denominator, -1, self.field_prime)) % self.field_prime
            result = (result + yi * lagrange_coeff) % self.field_prime
        return result
    
    def polynomial_to_blob(self, coefficients: List[int]) -> bytes:
        blob_elements = [0] * 4096
        for i, coeff in enumerate(coefficients):
            if i < 4096:
                blob_elements[i] = coeff % self.field_prime
        
        blob_bytes = b''
        for element in blob_elements:
            element_bytes = element.to_bytes(32, 'little')
            blob_bytes += element_bytes
        
        return blob_bytes