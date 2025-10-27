"""
Test suite for Elliptic Curve Cryptography implementation
"""

import elliptic_curve
import da_vinci_code


def test_elliptic_curve_creation():
    """Test creating an elliptic curve"""
    # Valid curve
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    assert curve.a == 2
    assert curve.b == 3
    assert curve.p == 97
    
    # Test singular curve rejection
    try:
        # This should raise ValueError (singular curve)
        singular = elliptic_curve.EllipticCurve(a=0, b=0, p=97)
        assert False, "Should have raised ValueError for singular curve"
    except ValueError:
        pass


def test_point_on_curve():
    """Test checking if a point is on the curve"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    
    # Test a valid point (3, 6) on y² = x³ + 2x + 3 (mod 97)
    # 6² = 36, 3³ + 2*3 + 3 = 27 + 6 + 3 = 36
    assert curve.is_on_curve(3, 6) == True
    
    # Test an invalid point
    assert curve.is_on_curve(1, 1) == False


def test_point_creation():
    """Test creating points on an elliptic curve"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    
    # Valid point
    point = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    assert point.x == 3
    assert point.y == 6
    
    # Point at infinity
    inf = elliptic_curve.EllipticCurvePoint(None, None, curve)
    assert inf.is_at_infinity() == True
    
    # Invalid point should raise error
    try:
        invalid = elliptic_curve.EllipticCurvePoint(1, 1, curve)
        assert False, "Should have raised ValueError for invalid point"
    except ValueError:
        pass


def test_point_addition():
    """Test elliptic curve point addition"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    
    # Create points
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    Q = elliptic_curve.EllipticCurvePoint(80, 10, curve)
    O = elliptic_curve.EllipticCurvePoint(None, None, curve)  # Point at infinity
    
    # Test P + O = P
    result = P + O
    assert result == P
    
    # Test O + P = P
    result = O + P
    assert result == P
    
    # Test P + Q
    result = P + Q
    assert result.x is not None
    assert result.y is not None


def test_point_doubling():
    """Test elliptic curve point doubling (P + P)"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    
    # Test P + P = 2P
    result = P + P
    assert result.x is not None
    assert result.y is not None
    
    # Verify it's on the curve
    assert curve.is_on_curve(result.x, result.y)


def test_scalar_multiplication():
    """Test scalar multiplication of points"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    
    # Test 0 * P = O
    result = P * 0
    assert result.is_at_infinity()
    
    # Test 1 * P = P
    result = P * 1
    assert result == P
    
    # Test 2 * P = P + P
    result1 = P * 2
    result2 = P + P
    assert result1 == result2
    
    # Test 3 * P = P + P + P
    result1 = P * 3
    result2 = P + P + P
    assert result1 == result2
    
    # Test larger scalar
    result = P * 10
    assert result.x is not None or result.is_at_infinity()


def test_divine_curve():
    """Test the divine curve creation"""
    curve = elliptic_curve.divine_curve()
    
    # Verify it's a valid elliptic curve
    assert curve.p > 0
    assert curve.a >= 0
    assert curve.b >= 0
    
    # Verify it uses Phi-inspired parameters
    phi = da_vinci_code.golden_ratio(100)
    assert curve.a == int(phi)  # Should be 1


def test_find_generator_point():
    """Test finding a generator point on the curve"""
    curve = elliptic_curve.divine_curve()
    
    # Find a generator
    generator = elliptic_curve._find_generator_point(curve)
    
    # Verify it's a valid point on the curve
    assert not generator.is_at_infinity()
    assert curve.is_on_curve(generator.x, generator.y)


def test_keypair_generation():
    """Test cryptographic key pair generation"""
    curve = elliptic_curve.divine_curve()
    generator = elliptic_curve._find_generator_point(curve)
    
    # Generate keypair
    private_key, public_key = elliptic_curve.generate_divine_keypair(curve, generator)
    
    # Verify private key is a valid integer
    assert isinstance(private_key, int)
    assert 0 < private_key < curve.p
    
    # Verify public key is a valid point on the curve
    assert isinstance(public_key, elliptic_curve.EllipticCurvePoint)
    assert not public_key.is_at_infinity()
    assert curve.is_on_curve(public_key.x, public_key.y)
    
    # Verify public_key = private_key * generator
    expected_public = generator * private_key
    assert public_key == expected_public


def test_encryption_decryption():
    """Test elliptic curve encryption and decryption"""
    # Setup
    curve = elliptic_curve.divine_curve()
    generator = elliptic_curve._find_generator_point(curve)
    private_key, public_key = elliptic_curve.generate_divine_keypair(curve, generator)
    
    # Test with a simple message
    message = 5
    
    # Encrypt
    C1, C2 = elliptic_curve.divine_encrypt(message, public_key, generator)
    
    # Verify ciphertexts are valid points
    assert isinstance(C1, elliptic_curve.EllipticCurvePoint)
    assert isinstance(C2, elliptic_curve.EllipticCurvePoint)
    assert not C1.is_at_infinity()
    assert not C2.is_at_infinity()
    
    # Decrypt
    decrypted_point = elliptic_curve.divine_decrypt(C1, C2, private_key)
    
    # Verify decryption produces a valid point
    assert isinstance(decrypted_point, elliptic_curve.EllipticCurvePoint)
    
    # The decrypted point should equal message * generator
    expected_point = generator * message
    assert decrypted_point == expected_point


def test_point_negation():
    """Test that P + (-P) = O"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    
    # Create -P (same x, negated y)
    neg_P = elliptic_curve.EllipticCurvePoint(P.x, (-P.y) % curve.p, curve)
    
    # P + (-P) should be point at infinity
    result = P + neg_P
    assert result.is_at_infinity()


def test_associativity():
    """Test that point addition is associative: (P + Q) + R = P + (Q + R)"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    Q = elliptic_curve.EllipticCurvePoint(80, 10, curve)
    R = elliptic_curve.EllipticCurvePoint(80, 87, curve)
    
    left = (P + Q) + R
    right = P + (Q + R)
    
    assert left == right


def test_commutativity():
    """Test that point addition is commutative: P + Q = Q + P"""
    curve = elliptic_curve.EllipticCurve(a=2, b=3, p=97)
    
    P = elliptic_curve.EllipticCurvePoint(3, 6, curve)
    Q = elliptic_curve.EllipticCurvePoint(80, 10, curve)
    
    left = P + Q
    right = Q + P
    
    assert left == right


def test_tonelli_shanks():
    """Test the Tonelli-Shanks square root algorithm"""
    # Test case where square root exists
    # 4 is a quadratic residue mod 97, sqrt(4) = 2 or 95
    result = elliptic_curve._tonelli_shanks(4, 97)
    assert result is not None
    assert (result * result) % 97 == 4
    
    # Test case where square root doesn't exist
    # Not all numbers are quadratic residues
    result = elliptic_curve._tonelli_shanks(3, 97)
    # This may or may not have a square root, just verify it doesn't crash


if __name__ == "__main__":
    # Run all tests
    test_elliptic_curve_creation()
    print("✓ Elliptic curve creation tests passed")
    
    test_point_on_curve()
    print("✓ Point on curve tests passed")
    
    test_point_creation()
    print("✓ Point creation tests passed")
    
    test_point_addition()
    print("✓ Point addition tests passed")
    
    test_point_doubling()
    print("✓ Point doubling tests passed")
    
    test_scalar_multiplication()
    print("✓ Scalar multiplication tests passed")
    
    test_divine_curve()
    print("✓ Divine curve tests passed")
    
    test_find_generator_point()
    print("✓ Generator point tests passed")
    
    test_keypair_generation()
    print("✓ Keypair generation tests passed")
    
    test_encryption_decryption()
    print("✓ Encryption/decryption tests passed")
    
    test_point_negation()
    print("✓ Point negation tests passed")
    
    test_associativity()
    print("✓ Associativity tests passed")
    
    test_commutativity()
    print("✓ Commutativity tests passed")
    
    test_tonelli_shanks()
    print("✓ Tonelli-Shanks tests passed")
    
    print("\nAll tests passed successfully! ✓")
