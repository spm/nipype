# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from nipype.interfaces import utility


def test_csvReader(tmpdir):
    header = "files,labels,erosion\n"
    lines = ["foo,hello,300.1\n", "bar,world,5\n", "baz,goodbye,0.3\n"]
    for x in range(2):
        name = tmpdir.join("testfile.csv").strpath
        with open(name, "w") as fid:
            reader = utility.CSVReader()
            if x % 2 == 0:
                fid.write(header)
                reader.inputs.header = True
            fid.writelines(lines)
            fid.flush()
            reader.inputs.in_file = name
            out = reader.run()
            if x % 2 == 0:
                assert out.outputs.files == ["foo", "bar", "baz"]
                assert out.outputs.labels == ["hello", "world", "goodbye"]
                assert out.outputs.erosion == ["300.1", "5", "0.3"]
            else:
                assert out.outputs.column_0 == ["foo", "bar", "baz"]
                assert out.outputs.column_1 == ["hello", "world", "goodbye"]
                assert out.outputs.column_2 == ["300.1", "5", "0.3"]


def test_csvReader_quoted(tmpdir):
    lines = ['foo,"hello, world",300.1\n']

    name = tmpdir.join("testfile.csv").strpath
    with open(name, "w") as fid:
        reader = utility.CSVReader()
        fid.writelines(lines)
        fid.flush()
        reader.inputs.in_file = name
        out = reader.run()

        assert out.outputs.column_0 == ["foo"]
        assert out.outputs.column_1 == ["hello, world"]
        assert out.outputs.column_2 == ["300.1"]


def test_csvReader_tabs(tmpdir):
    header = "files\tlabels\terosion\n"
    lines = ["foo\thello\t300.1\n", "bar\tworld\t5\n", "baz\tgoodbye\t0.3\n"]
    for x in range(2):
        name = tmpdir.join("testfile.csv").strpath
        with open(name, "w") as fid:
            reader = utility.CSVReader(delimiter="\t")
            if x % 2 == 0:
                fid.write(header)
                reader.inputs.header = True
            fid.writelines(lines)
            fid.flush()
            reader.inputs.in_file = name
            out = reader.run()
            if x % 2 == 0:
                assert out.outputs.files == ["foo", "bar", "baz"]
                assert out.outputs.labels == ["hello", "world", "goodbye"]
                assert out.outputs.erosion == ["300.1", "5", "0.3"]
            else:
                assert out.outputs.column_0 == ["foo", "bar", "baz"]
                assert out.outputs.column_1 == ["hello", "world", "goodbye"]
                assert out.outputs.column_2 == ["300.1", "5", "0.3"]
