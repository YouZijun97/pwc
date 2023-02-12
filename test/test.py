import json
from pathlib import Path

base_dir_path = Path(__file__).parent.parent.absolute()
data_dir_path = base_dir_path / 'test' / 'data'
import sys

sys.path.insert(0, str(base_dir_path))
from src.entry import run

for sample in range(2):
    data = (data_dir_path / str(sample)).read_text(encoding='UTF-8')

    result = run(data)
    (data_dir_path / f'{sample}.result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=4),encoding='UTF-8'
    )

    result = json.loads((data_dir_path / f'{sample}.result.json').read_text(encoding='UTF-8'))
    answer = json.loads((data_dir_path / f'{sample}.answer.json').read_text(encoding='UTF-8'))
    print("No Problem!")
