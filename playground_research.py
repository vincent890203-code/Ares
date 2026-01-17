from Ares.departments.Research.scout import PubMedScout

def test_scout():
    print("PubMed 偵查兵出發...")
    scout = PubMedScout(headless=True) # 如果想看瀏覽器跳出來，改 False
    try:
        results = scout.search("LLM in healthcare", limit=3)
        for i, paper in enumerate(results, 1):
            print(f"\n論文 {i}: {paper['title']}")
            print(f"連結: {paper['link']}")
            print(f"摘要片段: {paper['snippet'][:50]}...")
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        scout.close()
        print("\n偵查結束")

if __name__ == "__main__":
    test_scout()