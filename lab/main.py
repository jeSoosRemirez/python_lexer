from modules.lexer import Lexer
from modules.parser import Parser


def test_parser():
    text = """
    if (x < 1) {
        return x + 1;
    } else {
        return x - 1;
    }
    // This is a comment
    /* This is a 
       multi-line comment */
    "string with \\"escaped quotes\\" and new\\nlines";
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    try:
        ast = parser.parse()
        for stmt in ast:
            print(stmt)
    except Exception as e:
        print(f"Error: {str(e)}")


test_parser()
