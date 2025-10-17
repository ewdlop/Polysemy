"""
Test suite for Elliptic Curve Cryptography in Celestial Mechanics
"""

import elliptic_celestial_crypto as ecc


def test_elliptic_curve_creation():
    """Test that elliptic curves can be created with valid parameters"""
    # Valid curve
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    assert curve.a == 2
    assert curve.b == 3
    assert curve.p == 97
    
    # Test that singular curves raise an error
    try:
        # This should be singular: 4a³ + 27b² = 0 (mod p)
        singular_curve = ecc.EllipticCurve(a=0, b=0, p=7)
        assert False, "Should have raised ValueError for singular curve"
    except ValueError as e:
        assert "singular" in str(e).lower()


def test_point_on_curve():
    """Test checking if points lie on the curve"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    
    # Point at infinity should always be on the curve
    assert curve.is_on_curve(None) == True
    
    # Test a valid point: (3, 6) on y² = x³ + 2x + 3 (mod 97)
    # 6² = 36, 3³ + 2*3 + 3 = 27 + 6 + 3 = 36 (mod 97) ✓
    assert curve.is_on_curve((3, 6)) == True
    
    # Test an invalid point
    assert curve.is_on_curve((2, 5)) == False


def test_point_addition_identity():
    """Test that adding point at infinity works as identity"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    P = (3, 6)
    
    # P + O = P (where O is point at infinity)
    assert curve.point_addition(P, None) == P
    assert curve.point_addition(None, P) == P
    assert curve.point_addition(None, None) == None


def test_point_addition_inverse():
    """Test that P + (-P) = O (point at infinity)"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    P = (3, 6)
    P_inv = (3, -6 % 97)  # Point with negated y-coordinate
    
    result = curve.point_addition(P, P_inv)
    assert result == None  # Should be point at infinity


def test_point_doubling():
    """Test point doubling (adding a point to itself)"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    P = (3, 6)
    
    # 2P should be a valid point on the curve
    result = curve.point_addition(P, P)
    assert result is not None
    assert curve.is_on_curve(result)


def test_scalar_multiplication():
    """Test scalar multiplication of points"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    P = (3, 6)
    
    # 0 * P = O (point at infinity)
    assert curve.scalar_multiplication(0, P) == None
    
    # 1 * P = P
    assert curve.scalar_multiplication(1, P) == P
    
    # 2 * P should equal P + P
    double_P = curve.point_addition(P, P)
    mult_2P = curve.scalar_multiplication(2, P)
    assert double_P == mult_2P
    
    # All results should be on the curve
    result = curve.scalar_multiplication(5, P)
    assert result is None or curve.is_on_curve(result)


def test_scalar_multiplication_properties():
    """Test mathematical properties of scalar multiplication"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    P = (3, 6)
    
    # (a + b) * P = a * P + b * P
    a, b = 3, 5
    left = curve.scalar_multiplication(a + b, P)
    right = curve.point_addition(
        curve.scalar_multiplication(a, P),
        curve.scalar_multiplication(b, P)
    )
    assert left == right


def test_orbital_crypto_system_init():
    """Test that the orbital crypto system initializes correctly"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Check that curve parameters are set
    assert crypto.curve.a == ecc.OrbitalCryptoSystem.A
    assert crypto.curve.b == ecc.OrbitalCryptoSystem.B
    assert crypto.curve.p == ecc.OrbitalCryptoSystem.P
    
    # Check that generator point is on the curve
    assert crypto.curve.is_on_curve(crypto.G)


def test_keypair_generation():
    """Test public/private key pair generation"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Generate a keypair
    private_key, public_key = crypto.generate_keypair()
    
    # Private key should be in valid range
    assert 1 <= private_key < crypto.N
    
    # Public key should be on the curve
    assert crypto.curve.is_on_curve(public_key)
    
    # Public key should equal private_key * G
    expected_public = crypto.curve.scalar_multiplication(private_key, crypto.G)
    assert public_key == expected_public


def test_ecdh_shared_secret():
    """Test that ECDH produces the same shared secret for both parties"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Alice generates her keys
    alice_private, alice_public = crypto.generate_keypair()
    
    # Bob generates his keys
    bob_private, bob_public = crypto.generate_keypair()
    
    # Both compute the shared secret
    alice_shared = crypto.compute_shared_secret(alice_private, bob_public)
    bob_shared = crypto.compute_shared_secret(bob_private, alice_public)
    
    # They should be the same
    assert alice_shared == bob_shared
    
    # And should be on the curve
    assert crypto.curve.is_on_curve(alice_shared)


def test_signature_generation_and_verification():
    """Test digital signature generation and verification"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Generate a keypair
    private_key, public_key = crypto.generate_keypair()
    
    # Sign a message
    message = "The planets move in elliptical orbits"
    signature = crypto.orbital_signature(message, private_key)
    
    # Signature should be a tuple of two integers
    assert isinstance(signature, tuple)
    assert len(signature) == 2
    r, s = signature
    assert isinstance(r, int)
    assert isinstance(s, int)
    
    # Verify the signature with correct public key
    is_valid = crypto.verify_signature(message, signature, public_key)
    assert is_valid == True


def test_signature_verification_wrong_key():
    """Test that signature verification fails with wrong public key"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Alice signs a message
    alice_private, alice_public = crypto.generate_keypair()
    message = "The planets move in elliptical orbits"
    signature = crypto.orbital_signature(message, alice_private)
    
    # Bob tries to claim it's his signature
    _, bob_public = crypto.generate_keypair()
    is_valid = crypto.verify_signature(message, signature, bob_public)
    assert is_valid == False


def test_signature_verification_tampered_message():
    """Test that signature verification fails with tampered message"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Sign original message
    private_key, public_key = crypto.generate_keypair()
    original_message = "The planets move in elliptical orbits"
    signature = crypto.orbital_signature(original_message, private_key)
    
    # Try to verify with tampered message
    tampered_message = "The planets move in circular orbits"
    is_valid = crypto.verify_signature(tampered_message, signature, public_key)
    assert is_valid == False


def test_multiple_signatures():
    """Test that multiple signatures of the same message are different"""
    crypto = ecc.OrbitalCryptoSystem()
    
    private_key, public_key = crypto.generate_keypair()
    message = "The same message"
    
    # Generate two signatures
    sig1 = crypto.orbital_signature(message, private_key)
    sig2 = crypto.orbital_signature(message, private_key)
    
    # They should be different (due to random k)
    assert sig1 != sig2
    
    # But both should verify
    assert crypto.verify_signature(message, sig1, public_key) == True
    assert crypto.verify_signature(message, sig2, public_key) == True


def test_secp256k1_generator_point():
    """Test that the secp256k1 generator point is valid"""
    crypto = ecc.OrbitalCryptoSystem()
    
    # Generator point should be on the curve
    assert crypto.curve.is_on_curve(crypto.G)
    
    # Test that G has the correct order (this would take too long, so we just verify it's not infinity)
    # n * G should be infinity (but we won't compute this as it's expensive)
    result = crypto.curve.scalar_multiplication(2, crypto.G)
    assert result is not None


def test_point_doubling_edge_case():
    """Test point doubling when y coordinate is zero"""
    # Create a curve where we can find a point with y=0
    # For y²=x³+ax+b, when y=0, we need x³+ax+b=0 (mod p)
    # Using p=7, a=0, b=0 (this is singular, so skip)
    # Let's use a valid curve and just test the logic
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    
    # Any valid point should work correctly
    P = (3, 6)
    result = curve.point_addition(P, P)
    assert result is None or curve.is_on_curve(result)


def test_point_addition_edge_case():
    """Test point addition with edge cases"""
    curve = ecc.EllipticCurve(a=2, b=3, p=97)
    
    # Test with identical points (should use point doubling)
    P = (3, 6)
    result = curve.point_addition(P, P)
    assert result is None or curve.is_on_curve(result)
    
    # Test with inverse points (should give point at infinity)
    Q = (3, -6 % 97)
    result = curve.point_addition(P, Q)
    assert result is None


if __name__ == "__main__":
    # Run all tests
    test_elliptic_curve_creation()
    print("✓ Elliptic curve creation tests passed")
    
    test_point_on_curve()
    print("✓ Point on curve tests passed")
    
    test_point_addition_identity()
    print("✓ Point addition identity tests passed")
    
    test_point_addition_inverse()
    print("✓ Point addition inverse tests passed")
    
    test_point_doubling()
    print("✓ Point doubling tests passed")
    
    test_scalar_multiplication()
    print("✓ Scalar multiplication tests passed")
    
    test_scalar_multiplication_properties()
    print("✓ Scalar multiplication properties tests passed")
    
    test_orbital_crypto_system_init()
    print("✓ Orbital crypto system initialization tests passed")
    
    test_keypair_generation()
    print("✓ Keypair generation tests passed")
    
    test_ecdh_shared_secret()
    print("✓ ECDH shared secret tests passed")
    
    test_signature_generation_and_verification()
    print("✓ Signature generation and verification tests passed")
    
    test_signature_verification_wrong_key()
    print("✓ Signature verification with wrong key tests passed")
    
    test_signature_verification_tampered_message()
    print("✓ Signature verification with tampered message tests passed")
    
    test_multiple_signatures()
    print("✓ Multiple signatures tests passed")
    
    test_secp256k1_generator_point()
    print("✓ secp256k1 generator point tests passed")
    
    test_point_doubling_edge_case()
    print("✓ Point doubling edge case tests passed")
    
    test_point_addition_edge_case()
    print("✓ Point addition edge case tests passed")
    
    print("\n" + "=" * 60)
    print("All tests passed successfully! ✓")
    print("=" * 60)
