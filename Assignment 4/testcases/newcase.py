from hash_table import *

def test_hash_set():
    print("\n=== Testing HashSet Implementation ===")
    
    def test_chaining():
        print("\nTesting Chaining Collision Handling:")
        
        # Test different table sizes
        for size in [7, 11, 23]:  # Small, medium, prime sizes
            print(f"\nTesting with table size {size}")
            params = (31, size)  # z = 31
            hash_set = HashSet("Chain", params)
            
            # Test 1: Basic insertions and finds
            print("Test 1: Basic operations")
            test_keys = ["a", "z", "A", "Z"]  # Edge cases for single chars
            for key in test_keys:
                hash_set.insert(key)
                assert hash_set.find(key), f"Failed to find inserted element '{key}'"
            
            # Test 2: Collision handling with similar strings
            print("Test 2: Collision handling")
            collision_keys = [
                "abc", "cba",  # Anagrams
                "aaa", "bbb",  # Similar patterns
                "abcde", "edcba",  # Longer anagrams
                "AaAa", "aAaA"  # Mixed case
            ]
            for key in collision_keys:
                hash_set.insert(key)
                assert hash_set.find(key), f"Failed to find collided element '{key}'"
            
            # Test 3: Load factor with longer strings
            print("Test 3: Load factor stress test")
            long_strings = [
                "abcdefghij",
                "ABCDEFGHIJ",
                "aAbBcCdDeE",
                "zZyYxXwWvV"
            ]
            initial_load = hash_set.get_load()
            for key in long_strings:
                hash_set.insert(key)
                assert hash_set.find(key), f"Failed to find long string '{key}'"
            assert hash_set.get_load() > initial_load, "Load factor not increasing"
            print(f"Load factor: {hash_set.get_load():.2f}")
            print(f"Final state: {hash_set}")
        
        print("Chaining tests passed!")

    def test_linear_probing():
        print("\nTesting Linear Probing:")
        
        # Test different table sizes
        for size in [11, 17, 31]:  # Various prime sizes
            print(f"\nTesting with table size {size}")
            params = (31, size)  # z = 31
            hash_set = HashSet("Linear", params)
            
            # Test 1: Basic operations with edge case characters
            print("Test 1: Basic operations")
            edge_chars = ["a", "z", "A", "Z", "m", "M"]
            for char in edge_chars:
                hash_set.insert(char)
                assert hash_set.find(char), f"Failed to find basic char '{char}'"
            
            # Test 2: Collision sequence with calculated collisions
            print("Test 2: Planned collision sequence")
            # These patterns might hash to same/consecutive slots
            collision_patterns = [
                "abc", "bcd", "cde",  # Sequential patterns
                "aaa", "bbb", "ccc",  # Repeated patterns
                "ABCD", "BCDE", "CDEF"  # Upper case sequences
            ]
            for pattern in collision_patterns:
                #print('hi',pattern)
                try:
                    hash_set.insert(pattern)
                    #print('yo',hash_set.find(pattern),pattern)
                    assert hash_set.find(pattern), f"Failed to find collided pattern '{pattern}'"
                except Exception as e:
                    # print('hiroshima')
                    print(f"Table full at pattern '{pattern}' as expected")
                    break
            
            # Test 3: Load factor approach to full table
            print("Test 3: Near-full table behavior")
            try:
                # Try to fill remaining slots with varied length strings
                test_strings = [
                    "aB", "cD", "eF", "gH",
                    "iJkL", "mNoP", "qRsT",
                    "uVwXyZ", "AbCdEf"
                ]
                for s in test_strings:
                    hash_set.insert(s)
                print(f"Load factor: {hash_set.get_load():.2f}")
            except Exception as e:
                print("Table full exception as expected")
            
            # Test 4: Find operations after filling
            print("Test 4: Comprehensive find tests")
            # Test finding elements across the probe sequence
            if hash_set.find("abc"):  # Only test if element was successfully inserted
                assert hash_set.find("bcd"), "Failed to find item in probe sequence"
            assert not hash_set.find("nonexistent"), "Found non-existent item"
            assert not hash_set.find("xyz"), "Found non-existent item"
            
            print(f"Final state: {hash_set}")
        
        print("Linear probing tests passed!")

    def test_double_hashing():
        print("\nTesting Double Hashing:")
        
        # Test different table sizes and parameters
        test_configs = [
            (31, 37, 7, 11),   # Small table
            (41, 43, 11, 17),  # Medium table
            (53, 59, 13, 23)   # Larger table
        ]
        
        for z1, z2, c2, size in test_configs:
            print(f"\nTesting with params z1={z1}, z2={z2}, c2={c2}, size={size}")
            params = (z1, z2, c2, size)
            hash_set = HashSet("Double", params)
            
            # Test 1: Basic insertions with varied lengths
            print("Test 1: Basic operations")
            basic_tests = [
                "a", "Z",  # Single chars
                "ab", "YZ",  # Two chars
                "abc", "XYZ",  # Three chars
                "abcd", "WXYZ"  # Four chars
            ]
            for key in basic_tests:
                hash_set.insert(key)
                assert hash_set.find(key), f"Failed to find basic test '{key}'"
            
            # Test 2: Collision handling with similar patterns
            print("Test 2: Collision patterns")
            collision_tests = [
                "aaa", "bbb", "ccc",  # Similar patterns
                "AAAA", "BBBB", "CCCC",  # Upper case patterns
                "aAaA", "bBbB", "cCcC"  # Mixed patterns
            ]
            for key in collision_tests:
                try:
                    hash_set.insert(key)
                    assert hash_set.find(key), f"Failed to find collision test '{key}'"
                except Exception:
                    print(f"Table full at '{key}' as expected")
                    break
            
            # Test 3: Stress test with longer strings
            print("Test 3: Stress test")
            stress_tests = [
                "abcdefgh", "ABCDEFGH",
                "aAbBcCdD", "zZyYxXwW",
                "abcABCabc", "xyzXYZxyz"
            ]
            for key in stress_tests:
                try:
                    hash_set.insert(key)
                    assert hash_set.find(key), f"Failed to find stress test '{key}'"
                except Exception:
                    print("Table full exception as expected")
                    break
            
            print(f"Final state: {hash_set}")
            print(f"Final load factor: {hash_set.get_load():.2f}")
        
        print("Double hashing tests passed!")

    # Run all HashSet tests
    test_chaining()
    test_linear_probing()
    test_double_hashing()

def test_hash_map():
    print("\n=== Testing HashMap Implementation ===")
    
    def test_chaining():
        print("\nTesting Chaining:")
        
        # Test different table sizes
        for size in [7, 13, 19]:
            print(f"\nTesting with table size {size}")
            params = (31, size)
            hash_map = HashMap("Chain", params)
            
            # Test 1: Basic operations with edge cases
            print("Test 1: Basic operations")
            edge_cases = [
                ("a", 1), ("z", 26),
                ("A", 27), ("Z", 52),
                ("m", 13), ("M", 39)
            ]
            for key, value in edge_cases:
                hash_map.insert((key, value))
                assert hash_map.find(key) == value, f"Basic insert/find failed for '{key}'"
            assert hash_map.find("nonexistent") is None, "Found non-existent key"
            
            # Test 2: Collision handling
            print("Test 2: Collision handling")
            collision_cases = [
                ("abc", "first"), ("cba", "second"),  # Anagrams
                ("AAA", "upper"), ("aaa", "lower"),   # Case variations
                ("XYZ", "end"), ("ZYX", "reverse")    # More anagrams
            ]
            for key, value in collision_cases:
                hash_map.insert((key, value))
                assert hash_map.find(key) == value, f"Collision insert/find failed for '{key}'"
            
            # Test 3: Complex keys with mixed case
            print("Test 3: Complex key patterns")
            complex_cases = [
                ("aAbB", 1), ("BbAa", 2),
                ("abcABC", 3), ("ABCabc", 4),
                ("zZzZzZ", 5), ("ZzZzZz", 6)
            ]
            for key, value in complex_cases:
                hash_map.insert((key, value))
                assert hash_map.find(key) == value, f"Complex key insert/find failed for '{key}'"
            
            print(f"Final state: {hash_map}")
            print(f"Load factor: {hash_map.get_load():.2f}")
        
        print("Chaining tests passed!")

    def test_linear_probing():
        print("\nTesting Linear Probing:")
        
        # Test different table sizes
        for size in [11, 17, 23]:
            print(f"\nTesting with table size {size}")
            params = (31, size)
            hash_map = HashMap("Linear", params)
            
            # Test 1: Single character keys
            print("Test 1: Single character keys")
            single_chars = [
                ("a", "alpha"), ("z", "zulu"),
                ("A", "ALPHA"), ("Z", "ZULU"),
                ("m", "mike"), ("M", "MIKE")
            ]
            for key, value in single_chars:
                hash_map.insert((key, value))
                assert hash_map.find(key) == value, f"Single char failed for '{key}'"
            
            # Test 2: Collision sequence
            print("Test 2: Collision sequence")
            collision_sequence = [
                ("abc", 100), ("bcd", 200),   # Sequential
                ("aaa", 300), ("bbb", 400),   # Repeated
                ("ABC", 500), ("BCD", 600)    # Upper case
            ]
            for key, value in collision_sequence:
                try:
                    hash_map.insert((key, value))
                    assert hash_map.find(key) == value, f"Collision sequence failed for '{key}'"
                except Exception:
                    print(f"Table full at '{key}' as expected")
                    break
            
            # Test 3: Long keys
            print("Test 3: Long key patterns")
            long_keys = [
                ("abcdefg", 1000),
                ("ABCDEFG", 2000),
                ("aAbBcCd", 3000),
                ("zZyYxXw", 4000)
            ]
            for key, value in long_keys:
                try:
                    hash_map.insert((key, value))
                    assert hash_map.find(key) == value, f"Long key failed for '{key}'"
                except Exception:
                    print("Table full exception as expected")
                    break
            
            print(f"Final state: {hash_map}")
            print(f"Load factor: {hash_map.get_load():.2f}")
        
        print("Linear probing tests passed!")

    def test_double_hashing():
        print("\nTesting Double Hashing:")
        
        # Test different configurations
        configs = [
            (31, 37, 7, 11),   # Small table
            (41, 43, 11, 17),  # Medium table
            (53, 59, 13, 23)   # Larger table
        ]
        
        for z1, z2, c2, size in configs:
            print(f"\nTesting with params z1={z1}, z2={z2}, c2={c2}, size={size}")
            params = (z1, z2, c2, size)
            hash_map = HashMap("Double", params)
            
            # Test 1: Edge case keys
            print("Test 1: Edge cases")
            edge_cases = [
                ("a", 1), ("z", 26),
                ("A", 27), ("Z", 52),
                ("aA", 53), ("zZ", 78)
            ]
            for key, value in edge_cases:
                hash_map.insert((key, value))
                assert hash_map.find(key) == value, f"Edge case failed for '{key}'"
            
            # Test 2: Systematic collision patterns
            print("Test 2: Collision patterns")
            collision_patterns = [
                ("aaa", "triple_a"),
                ("bbb", "triple_b"),
                ("AAA", "TRIPLE_A"),
                ("BBB", "TRIPLE_B")
            ]
            for key, value in collision_patterns:
                try:
                    hash_map.insert((key, value))
                    assert hash_map.find(key) == value, f"Collision pattern failed for '{key}'"
                except Exception:
                    print(f"Table full at '{key}' as expected")
                    break
            
            # Test 3: Mixed case and length variations
            print("Test 3: Mixed variations")
            variations = [
                ("aAbBcC", 100),
                ("AbCdEf", 200),
                ("zYxWvU", 300),
                ("ZyXwVu", 400)
            ]
            for key, value in variations:
                try:
                    hash_map.insert((key, value))
                    assert hash_map.find(key) == value, f"Variation failed for '{key}'"
                except Exception:
                    print("Table full exception as expected")
                    break
            
            print(f"Final state: {hash_map}")
            print(f"Load factor: {hash_map.get_load():.2f}")
        
        print("Double hashing tests passed!")

    # Run all HashMap tests
    test_chaining()
    test_linear_probing()
    test_double_hashing()

def main():
    test_hash_set()
    test_hash_map()

main()