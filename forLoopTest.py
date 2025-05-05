def run_emoji_code(code: str):
    lines = code.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith(':repeat') and line.endswith(':'):
            try:
                count = int(line.split()[1].strip(':'))
            except (IndexError, ValueError):
                raise ValueError(f"Invalid repeat syntax on line {i + 1}")

            # Collect block
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != ':':
                block.append(lines[i])
                i += 1

            # Run the block `count` times
            for _ in range(count):
                for b_line in block:
                    if b_line.strip() == '👋':
                        print('👋')  # You could expand this to match more emojis

        i += 1


# Example usage
emoji_code = """
:repeat 3:
👋
👋
:
"""

run_emoji_code(emoji_code)
