import pandas as pd
import numpy as np
from typing import Iterable

# 安全にフラグを数値に変換する関数
def _to_int8_bool(s: pd.Series) -> pd.Series:
    # True/False/NA を 1/0 に（NAは0扱い）
    return s.fillna(False).astype(bool).astype('int8')

def _as_numeric(s: pd.Series | None) -> pd.Series | None:
    if s is None:
        return None
    return pd.to_numeric(s, errors='coerce')

def _col_or_false(df: pd.DataFrame, col: str) -> pd.Series:
    """
    指定列が存在すればその列を返し、存在しなければ False の Series を返す。
    dtype は元列を尊重（後段で _to_int8_bool などに渡す前提）。
    """
    if col in df.columns:
        return df[col]
    else:
        return pd.Series(False, index=df.index)

def _zscore(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    std = s.std()
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / std

def _safe_mean(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    cols_exist = [c for c in cols if c in df.columns]
    if not cols_exist:
        return pd.Series(0.0, index=df.index)
    return df[cols_exist].mean(axis=1).fillna(0.0)

def _safe_log1p(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors='coerce')
    x = x.where(x > -1, np.nan)
    return np.log1p(x)

def _get_or_zeros(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series(0.0, index=df.index)
    return df[col].astype(float).replace([np.inf, -np.inf], np.nan).fillna(0.0)

def _num0(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series(0.0, index=df.index)
    return pd.to_numeric(df[col], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0.0)

def _flag(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series(0, index=df.index, dtype='int8')
    return pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int8')

def _add(df: pd.DataFrame, name: str, s: pd.Series) -> None:
    df[name] = s.astype('float32')

def _existing_cols(df: pd.DataFrame, cols: Iterable[str]) -> list[str]:
    return [c for c in cols if c in df.columns]

def _sum_cols(df: pd.DataFrame, cols: list[str], out_col: str) -> pd.Series:
    if not cols:
        return pd.Series(np.zeros(len(df), dtype=np.float32), index=df.index, name=out_col)
    s = df[cols].fillna(0)
    # bool / int / float いずれでも合計できるようにする
    s = s.astype('float32')
    return s.sum(axis=1).rename(out_col)

def _any_cols(df: pd.DataFrame, cols: list[str], out_col: str) -> pd.Series:
    if not cols:
        return pd.Series(np.zeros(len(df), dtype=np.int8), index=df.index, name=out_col)
    s = df[cols].fillna(0).astype('float32')
    return (s.max(axis=1) > 0).astype('int8').rename(out_col)