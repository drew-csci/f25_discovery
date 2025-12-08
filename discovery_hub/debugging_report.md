Debugging Assignment:

Setup Summary:
    created virtual environment: python3 -m venv .venv
    activated venv: source .venv/bin/activate or
    installed dependencies: pip install -r requirements.txt
    configured VSCode debug in .vscode/launch.json for runserver and test debugging


Bug list and Explanation:
Bug 1: Attribute Error
    cause: .get('q') returns None so calling .strip() crashes
    found because of breakpoint on query = request.GET.get('q').strip()
    fix: (request.GET.get('q') or "").strip()

bug 2: Logic Bug (is vs ==)
    cause: is not 'All' checks object identity instead of equality
    found because of breakpoint on if field_filter is not 'All' observed wrong filtering
    fixed: if field_filter != 'All'

bug 3: Key Error
    cause: misspelled dictionary key 'descriptionn'
    found because of exception on filter predicate
    fix: corrected to 'description'

