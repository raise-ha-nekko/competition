import yaml
import pathlib


# 共通関数==================================
class Common:
    def __init__(self):
        YML_PATH = './config.yml'
    
        with open(YML_PATH, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
        self.config_data = yaml_data

        # 目的変数
        self.TARGET_COL = self.config_data['target_col']

        # ユニークキー変数
        self.UNIQUE_KEY_COLS = self.config_data['unique_key_cols']

        # 説明変数
        self.NUMERIC_COLS = self.config_data['numeric_cols']
        self.CATEGORY_COLS = self.config_data['category_cols']
        self.TRAIN_FEATURE_COLS = [self.TARGET_COL] + self.NUMERIC_COLS + [self.UNIQUE_KEY_COLS]
        self.TEST_FEATURE_COLS = self.NUMERIC_COLS + [self.UNIQUE_KEY_COLS]

        # 再生可能エネルギーのカラム
        self.SUS_GENE_COLS = self.config_data['sus_gene_cols']

        # ベースパス
        self.BASE_PATH = pathlib.Path(self.config_data['base_path'])

        # パスを正規化してから Path オブジェクトに変換（Windowsの \ 混入を防ぐ）
        clean_base_path = self.config_data['base_path'].replace('\\', '/')
        self.BASE_PATH = pathlib.Path(clean_base_path).expanduser().resolve()

        # コンペフォルダのパス
        self.SCRIPT_PATH = self.BASE_PATH / 'competition' / 'Signate' / '1634：SMBC_GREEN×DATA_Challenge_2025'

        # 共通関数のパス
        self.COMMON_FUNC_PATH = self.BASE_PATH / '共通関数'