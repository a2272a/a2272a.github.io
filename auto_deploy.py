#!/usr/bin/env python3
"""
🚀 가격표 완전 자동 업데이트 & 배포
엑셀 → CSV 변환 → Git 배포까지 한 번에!

사용법:
  python3 auto_deploy.py [엑셀파일경로]
  
예시:
  python3 auto_deploy.py 전기종특가.xlsx
  python3 auto_deploy.py  # 기본: uploaded_files 폴더에서 최신 파일 사용
"""

import pandas as pd
import sys
import os
import subprocess
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

def run_command(cmd, description):
    """명령어 실행"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd='/home/user/webapp'
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"명령어 실패: {cmd}")
        if e.stderr:
            print(e.stderr)
        return False

def find_latest_excel():
    """uploaded_files 폴더에서 가장 최근 엑셀 파일 찾기"""
    upload_dir = Path('/home/user/uploaded_files')
    if not upload_dir.exists():
        return None
    
    excel_files = list(upload_dir.glob('*.xlsx')) + list(upload_dir.glob('*.xls'))
    if not excel_files:
        return None
    
    latest_file = max(excel_files, key=lambda f: f.stat().st_mtime)
    return str(latest_file)

def convert_excel_to_csv(excel_path, output_path='data.csv'):
    """엑셀 파일을 CSV로 변환"""
    
    print_header("📊 엑셀 → CSV 변환")
    
    if not os.path.exists(excel_path):
        print_error(f"파일을 찾을 수 없습니다: {excel_path}")
        return False
    
    print_info(f"입력: {os.path.basename(excel_path)}")
    print_info(f"출력: {output_path}")
    
    try:
        df = pd.read_excel(excel_path, sheet_name=0)
        
        # CSV_출력 컬럼 찾기
        csv_col_index = None
        for i, col in enumerate(df.columns):
            if 'CSV_출력' in str(col) or 'CSV' in str(col):
                csv_col_index = i
                break
        
        if csv_col_index is None:
            print_warning("CSV_출력 컬럼 없음. 전체 데이터 사용")
            output_df = df
        else:
            output_df = df.iloc[:, csv_col_index:]
            output_df.columns = output_df.iloc[0]
            output_df = output_df[1:].reset_index(drop=True)
        
        output_df = output_df.dropna(how='all')
        output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print_success(f"변환 완료: {len(output_df)}행 x {len(output_df.columns)}열")
        return True
        
    except Exception as e:
        print_error(f"변환 실패: {e}")
        return False

def git_deploy():
    """Git으로 배포"""
    
    print_header("🚀 Git 배포")
    
    # Git 상태 확인
    if not run_command('git status', 'Git 상태 확인'):
        return False
    
    # 변경사항 추가
    if not run_command('git add data.csv', 'data.csv 추가'):
        return False
    
    # 커밋 메시지 생성
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_msg = f'update: 가격표 업데이트 ({timestamp})'
    
    # 커밋
    if not run_command(f'git commit -m "{commit_msg}"', '변경사항 커밋'):
        print_warning("변경사항이 없거나 커밋 실패")
        return False
    
    # 원격 동기화
    if not run_command('git fetch origin main', '원격 저장소 동기화'):
        return False
    
    # 리베이스
    if not run_command('git rebase origin/main', '최신 변경사항 병합'):
        print_warning("리베이스 실패. 충돌 해결 필요")
        return False
    
    # 푸시
    if not run_command('git push origin main', '원격 저장소에 푸시'):
        return False
    
    print_success("배포 완료!")
    return True

def main():
    print_header("🚀 가격표 자동 업데이트 & 배포")
    
    # 엑셀 파일 경로 결정
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    else:
        print_info("최신 엑셀 파일 검색 중...")
        excel_path = find_latest_excel()
        
        if not excel_path:
            print_error("엑셀 파일을 찾을 수 없습니다!")
            print_info("\n사용법: python3 auto_deploy.py [엑셀파일]")
            sys.exit(1)
        
        print_success(f"발견: {os.path.basename(excel_path)}")
    
    # 작업 디렉토리
    os.chdir('/home/user/webapp')
    
    # 1단계: 변환
    if not convert_excel_to_csv(excel_path, 'data.csv'):
        print_error("변환 실패")
        sys.exit(1)
    
    # 2단계: 배포
    print_info("\n배포를 진행하시겠습니까?")
    print_info("  Enter: 배포 진행")
    print_info("  Ctrl+C: 취소")
    
    try:
        input()
    except KeyboardInterrupt:
        print_warning("\n\n배포 취소됨")
        print_info("변환된 data.csv는 저장되었습니다.")
        sys.exit(0)
    
    if git_deploy():
        print_header("✅ 완료!")
        print_success("가격표가 성공적으로 배포되었습니다!")
        print_info("\n약 1-2분 후 사이트에 반영됩니다:")
        print_info("  👉 https://a2272a.github.io/")
        print_info("\n새로고침: Ctrl+F5 (강력 새로고침)")
    else:
        print_header("⚠️  부분 완료")
        print_warning("변환은 완료되었으나 배포 실패")
        print_info("\n수동 배포 명령어:")
        print_info("  git add data.csv")
        print_info("  git commit -m 'update: 가격표 업데이트'")
        print_info("  git push origin main")

if __name__ == '__main__':
    main()
