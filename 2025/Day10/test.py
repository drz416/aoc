# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "numpy",
# ]
# ///


def main() -> None:
    import numpy as np

    # (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}



    def gaussian_elimination(A, b):
        n = len(b)
        Ab = np.hstack([A, b.reshape(-1, 1)])
        
        for i in range(n):
            # Find pivot row (partial pivoting)
            max_index = i + np.argmax(np.abs(Ab[i:, i]))
            if Ab[max_index, i] == 0:
                raise ValueError("Matrix is singular or nearly singular; cannot solve.")
            # Swap rows
            Ab[[i, max_index]] = Ab[[max_index, i]]
            
            # Eliminate below
            for j in range(i+1, n):
                factor = Ab[j, i] / Ab[i, i]
                Ab[j, i:] -= factor * Ab[i, i:]
        
        # Back substitution
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            if Ab[i, i] == 0:
                raise ValueError("Zero pivot encountered during back substitution.")
            x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
        
        return x

    # Example usage
    A = np.array([[0, 0, 0, 0, 1, 1],
                  [0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 1, 1, 0],
                  [1, 1, 0, 1, 0, 0]], dtype=float)
    b = np.array([3, 5, 4, 7], dtype=float)

    solution = gaussian_elimination(A, b)
    print("Solution:", solution)


if __name__ == "__main__":
    main()
