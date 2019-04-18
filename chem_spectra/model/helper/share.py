import tempfile


def store_str_in_tmp(str_content, prefix='tmp', suffix='', directory=None):
    b_content = str.encode(str_content)
    return store_byte_in_tmp(b_content, suffix)


def store_byte_in_tmp(b_content, prefix='tmp', suffix='', directory=None):
    tf = tempfile.NamedTemporaryFile(
        prefix=prefix,
        suffix=suffix,
        dir=directory
    )
    with open(tf.name, 'w') as f:
        tf.write(b_content)
    tf.file.seek(0)
    return tf
