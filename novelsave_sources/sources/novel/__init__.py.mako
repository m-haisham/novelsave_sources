% for source in sources:
    from .${source.__module__.rsplit('.', maxsplit=1)[1]} import ${source.__name__}
% endfor

sources = [
    % for source in sources:
        ${source.__name__},
    % endfor
]
