#!/usr/bin/env python3
"""
🚀 가격표 자동 업데이트 스크립트
엑셀 파일을 CSV로 변환하고 자동으로 배포합니다.

사용법:
  python3 update_prices.py [엑셀파일경로]
  
예시:
  python3 update_prices.py 전기종특가.xlsx
  python3 update_prices.py  # 기본: uploaded_files 폴더에서 최신 파일 사용
"""

import pandas as pd
import sys
import os
from datetime import datetime
from pathlib import Path

# 색상 코드
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def find_latest_excel():
    """uploaded_files 폴더에서 가장 최근 엑셀 파일 찾기"""
    upload_dir = Path('/home/user/uploaded_files')
    if not upload_dir.exists():
        return None
    
    excel_files = list(upload_dir.glob('*.xlsx')) + list(upload_dir.glob('*.xls'))
    if not excel_files:
        return None
    
    # 가장 최근 파일 반환
    latest_file = max(excel_files, key=lambda f: f.stat().st_mtime)
    return str(latest_file)

def convert_excel_to_csv(excel_path, output_path='data.csv'):
    """엑셀 파일을 CSV로 변환"""
    
    print_header("📊 엑셀 → CSV 변환 시작")
    
    # 파일 존재 확인
    if not os.path.exists(excel_path):
        print_error(f"파일을 찾을 수 없습니다: {excel_path}")
        return False
    
    print_info(f"입력 파일: {excel_path}")
    print_info(f"출력 파일: {output_path}")
    
    try:
        # 엑셀 파일 읽기
        print_info("엑셀 파일 읽는 중...")
        df = pd.read_excel(excel_path, sheet_name=0)
        
        # 'CSV_출력(손대지마)' 컬럼부터 데이터 추출
        csv_col_index = None
        for i, col in enumerate(df.columns):
            if 'CSV_출력' in str(col) or 'CSV' in str(col):
                csv_col_index = i
                break
        
        if csv_col_index is None:
            print_warning("CSV_출력 컬럼을 찾을 수 없습니다. 전체 데이터를 사용합니다.")
            output_df = df
        else:
            print_success(f"CSV_출력 컬럼 발견 (인덱스: {csv_col_index})")
            # CSV_출력 컬럼부터 끝까지 추출
            output_df = df.iloc[:, csv_col_index:]
            
            # 첫 행을 헤더로 사용
            output_df.columns = output_df.iloc[0]
            output_df = output_df[1:].reset_index(drop=True)
        
        # 빈 행 제거
        output_df = output_df.dropna(how='all')
        
        # CSV로 저장
        print_info("CSV 파일로 저장 중...")
        output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        # 통계 출력
        print_success(f"변환 완료!")
        print_info(f"  📝 총 {len(output_df)}개 행")
        print_info(f"  📋 총 {len(output_df.columns)}개 컬럼")
        
        # 미리보기
        print_info("\n데이터 미리보기 (처음 3행):")
        print(output_df.head(3).to_string(max_colwidth=15))
        
        return True
        
    except Exception as e:
        print_error(f"변환 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

def backup_current_csv():
    """현재 data.csv를 백업"""
    if os.path.exists('data.csv'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'data.backup.{timestamp}.csv'
        os.rename('data.csv', backup_name)
        print_success(f"기존 파일 백업: {backup_name}")
        return True
    return False

def main():
    print_header("🚀 가격표 자동 업데이트")
    
    # 엑셀 파일 경로 결정
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    else:
        print_info("엑셀 파일 경로가 지정되지 않았습니다.")
        print_info("uploaded_files 폴더에서 최신 파일을 찾습니다...")
        excel_path = find_latest_excel()
        
        if not excel_path:
            print_error("엑셀 파일을 찾을 수 없습니다!")
            print_info("\n사용법:")
            print_info("  python3 update_prices.py [엑셀파일경로]")
            sys.exit(1)
        
        print_success(f"최신 파일 발견: {os.path.basename(excel_path)}")
    
    # 작업 디렉토리 변경
    os.chdir('/home/user/webapp')
    
    # 백업
    backup_current_csv()
    
    # 변환
    if convert_excel_to_csv(excel_path, 'data.csv'):
        print_header("✅ 완료!")
        print_success("가격표가 성공적으로 업데이트되었습니다!")
        print_info("\n다음 단계:")
        print_info("  1. 브라우저에서 사이트 새로고침 (Ctrl+F5)")
        print_info("  2. 가격이 올바르게 표시되는지 확인")
        print_info("  3. 문제없으면 Git으로 배포")
        print_info("\n배포 명령어:")
        print_info("  cd /home/user/webapp")
        print_info("  git add data.csv")
        print_info("  git commit -m 'update: 가격표 업데이트'")
        print_info("  git push origin main")
    else:
        print_header("❌ 실패")
        print_error("변환에 실패했습니다. 에러 메시지를 확인해주세요.")
        sys.exit(1)

if __name__ == '__main__':
    main()
