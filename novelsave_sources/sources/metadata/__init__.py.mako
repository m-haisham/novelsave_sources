% for source in meta_sources:
    from .${source.__module__.rsplit('.', maxsplit=1)[1]} import ${source.__name__}
% endfor

meta_sources = [
    % for source in meta_sources:
        ${source.__name__},
    % endfor
]
