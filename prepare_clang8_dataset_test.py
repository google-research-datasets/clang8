"""Tests for prepare_clang8_dataset."""

import os
from absl.testing import absltest

import prepare_clang8_dataset


class PrepareClang8DatasetTest(absltest.TestCase):

  def test_preparing_fake_clang8(self):
    lang8_dir = self.create_tempdir().full_path
    lang8_path = os.path.join(lang8_dir, 'lang-8-20111007-L1-v2.dat')
    with open(lang8_path, 'w') as f2:
      f2.write("""["123","111","Japanese","English","""
               """["This isn't gramatical.","This is"],[[],[]]]\n""")
      f2.write("""["123","222","Japanese","English",["A best"],[[]]]\n""")

    clang8_targets_dir = self.create_tempdir().full_path
    targets_path = os.path.join(clang8_targets_dir, 'clang8_en.detokenized.tsv')
    with open(targets_path, 'w') as f:
      f.write("123\t111\t0\tFalse\tThis isn't grammatical.\n")
      f.write('123\t111\t1\tFalse\tThis is\n')
      f.write('123\t222\t0\tTrue\tThe best\n')

    language = 'en'
    output_dir = self.create_tempdir().full_path
    prepare_clang8_dataset._prepare_clang8(
        language, clang8_targets_dir, lang8_dir, output_dir, tokenize_text=True)
    output_path = os.path.join(
        output_dir, f'clang8_source_target_{language}.spacy_tokenized.tsv')
    with open(output_path) as f:
      output_lines = f.readlines()
    self.assertEqual(output_lines, [
        "This is n't gramatical .\tThis is n't grammatical .\n",
        'This is\tThis is\n',
        'A best\tThe best\n',
    ])


if __name__ == '__main__':
  absltest.main()
