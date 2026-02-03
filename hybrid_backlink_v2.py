"""
Hybrid Backlink Analyzer V2
ادغام SeleniumBase + SE Ranking + Ahrefs Fallbacks
"""

from typing import List, Dict, Optional
import time

# SE Ranking API
from backlink_module import BacklinkAnalyzer

# SeleniumBase scraper
try:
    from ahrefs_seleniumbase import scrape_ahrefs_seleniumbase
    SELENIUMBASE_AVAILABLE = True
except ImportError:
    SELENIUMBASE_AVAILABLE = False
    print("⚠️ SeleniumBase در دسترس نیست - نصب کنید: pip install seleniumbase")


class HybridBacklinkAnalyzerV2:
    """
    ترکیب هوشمند چند منبع بک‌لینک
    
    اولویت:
    1. Ahrefs (SeleniumBase) - رایگان، 80-90% موفقیت
    2. SE Ranking API - پولی، 100% موفقیت
    3. Fallback strategies
    """
    
    def __init__(
        self,
        prefer_ahrefs: bool = False,
        use_seleniumbase: bool = True,
        headless: bool = False
    ):
        """
        Args:
            prefer_ahrefs: اولویت با Ahrefs یا SE Ranking
            use_seleniumbase: استفاده از SeleniumBase برای Ahrefs
            headless: مرورگر مخفی (برای production)
        """
        self.se_ranking = BacklinkAnalyzer()
        self.prefer_ahrefs = prefer_ahrefs
        self.use_seleniumbase = use_seleniumbase and SELENIUMBASE_AVAILABLE
        self.headless = headless
        
        if not SELENIUMBASE_AVAILABLE and use_seleniumbase:
            print("⚠️ SeleniumBase نصب نیست - فقط از SE Ranking استفاده می‌شود")
            self.use_seleniumbase = False
    
    def fetch_links(
        self,
        domain: str,
        limit: int = 100,
        fallback: bool = True,
        ahrefs_wait_time: int = 10
    ) -> List[Dict]:
        """
        دریافت بک‌لینک با استراتژی هوشمند
        
        Args:
            domain: دامنه مورد نظر
            limit: حداکثر تعداد بک‌لینک
            fallback: اگر منبع اول شکست خورد، از دیگری استفاده کند
            ahrefs_wait_time: زمان انتظار برای Ahrefs (ثانیه)
        
        Returns:
            لیست بک‌لینک‌ها
        """
        backlinks = []
        
        # تعیین اولویت منابع
        if self.prefer_ahrefs and self.use_seleniumbase:
            primary = "ahrefs_seleniumbase"
            secondary = "se_ranking"
        else:
            primary = "se_ranking"
            secondary = "ahrefs_seleniumbase" if self.use_seleniumbase else None
        
        print(f"🎯 استراتژی: اولویت با {primary}")
        
        # تلاش با منبع اول
        backlinks = self._fetch_from_source(
            domain,
            primary,
            limit,
            ahrefs_wait_time
        )
        
        # Fallback به منبع دوم
        if fallback and len(backlinks) < 10 and secondary:
            print(f"⚠️ تعداد کم ({len(backlinks)}). تلاش با {secondary}...")
            
            secondary_links = self._fetch_from_source(
                domain,
                secondary,
                limit,
                ahrefs_wait_time
            )
            
            # ترکیب نتایج
            backlinks = self._merge_backlinks(backlinks, secondary_links)
        
        # محدود کردن به limit
        return backlinks[:limit]
    
    def _fetch_from_source(
        self,
        domain: str,
        source: str,
        limit: int,
        ahrefs_wait_time: int
    ) -> List[Dict]:
        """دریافت از یک منبع خاص"""
        
        try:
            if source == "ahrefs_seleniumbase" and self.use_seleniumbase:
                print(f"🦊 دریافت از Ahrefs (SeleniumBase UC mode)...")
                
                backlinks = scrape_ahrefs_seleniumbase(
                    domain=domain,
                    headless=self.headless,
                    wait_time=ahrefs_wait_time
                )
                
                # نرمال‌سازی فرمت (تبدیل به فرمت استاندارد)
                return self._normalize_ahrefs_format(backlinks)
            
            elif source == "se_ranking":
                print(f"🔍 دریافت از SE Ranking API...")
                return self.se_ranking.fetch_links(domain, limit=limit)
            
            else:
                print(f"⚠️ منبع {source} در دسترس نیست")
                return []
        
        except Exception as e:
            print(f"❌ خطا در دریافت از {source}: {e}")
            return []
    
    def _normalize_ahrefs_format(self, ahrefs_data: List[Dict]) -> List[Dict]:
        """تبدیل فرمت Ahrefs به فرمت استاندارد"""
        normalized = []
        
        for link in ahrefs_data:
            try:
                # اگر از قبل normalized شده
                if "domain_inlink_rank" in link:
                    normalized.append(link)
                    continue
                
                # تبدیل فرمت
                normalized.append({
                    "url_from": link.get("url_from", "N/A"),
                    "url_to": link.get("url_to", "N/A"),
                    "anchor": link.get("anchor", "N/A"),
                    "nofollow": 1 if link.get("nofollow") else 0,
                    "domain_inlink_rank": link.get("domain_rating", "N/A"),
                    "first_seen": "N/A",
                    "source": link.get("source", "ahrefs"),
                    "inlink_rank": "N/A",
                    "page_inlink_rank": "N/A",
                })
            except Exception as e:
                print(f"⚠️ خطا در نرمال‌سازی: {e}")
                continue
        
        return normalized
    
    def _merge_backlinks(self, list1: List[Dict], list2: List[Dict]) -> List[Dict]:
        """ترکیب دو لیست و حذف تکراری‌ها"""
        merged = list1.copy()
        seen_urls = {link.get("url_from") for link in list1 if link.get("url_from")}
        
        for link in list2:
            url_from = link.get("url_from")
            if url_from and url_from not in seen_urls and url_from != "N/A":
                merged.append(link)
                seen_urls.add(url_from)
        
        return merged
    
    def fetch_with_quality_score(
        self,
        domain: str,
        limit: int = 100,
        ahrefs_wait_time: int = 10
    ) -> List[Dict]:
        """
        دریافت بک‌لینک‌ها با امتیاز کیفیت
        """
        print(f"\n🔬 تحلیل ترکیبی برای {domain}...")
        
        # دریافت از هر دو منبع (اگر ممکن باشد)
        all_backlinks = []
        
        if self.use_seleniumbase:
            ahrefs_links = self._fetch_from_source(
                domain,
                "ahrefs_seleniumbase",
                limit,
                ahrefs_wait_time
            )
            all_backlinks.extend(ahrefs_links)
            time.sleep(2)
        
        se_links = self._fetch_from_source(domain, "se_ranking", limit, 0)
        all_backlinks.extend(se_links)
        
        # حذف تکراری
        merged = self._merge_backlinks([], all_backlinks)
        
        # محاسبه Quality Score
        for link in merged:
            link["quality_score"] = self._calculate_quality_score(link)
        
        # مرتب‌سازی
        merged.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
        
        print(f"✅ کل بک‌لینک‌ها: {len(merged)}")
        
        return merged[:limit]
    
    def _calculate_quality_score(self, link: Dict) -> float:
        """محاسبه امتیاز کیفیت"""
        score = 0.0
        
        # Domain Rating
        dr = link.get("domain_inlink_rank", "N/A")
        if dr != "N/A":
            try:
                score += float(dr) * 2
            except:
                pass
        
        # Dofollow
        if link.get("nofollow") == 0:
            score += 20
        
        # Anchor Text
        anchor = link.get("anchor", "")
        if anchor and anchor != "N/A" and len(anchor) > 3:
            score += 10
        
        # Source bonus
        source = link.get("source", "")
        if "ahrefs" in source:
            score += 5
        
        return score


# =====================================
# Helper Functions برای استفاده آسان
# =====================================

def get_backlinks_hybrid(
    domain: str,
    use_ahrefs: bool = True,
    headless: bool = False,
    limit: int = 100
) -> List[Dict]:
    """
    Helper function ساده
    
    Args:
        domain: دامنه
        use_ahrefs: استفاده از Ahrefs SeleniumBase
        headless: مرورگر مخفی
        limit: حداکثر تعداد
    
    Returns:
        لیست بک‌لینک‌ها
    """
    analyzer = HybridBacklinkAnalyzerV2(
        prefer_ahrefs=use_ahrefs,
        use_seleniumbase=use_ahrefs,
        headless=headless
    )
    
    return analyzer.fetch_links(domain, limit=limit, fallback=True)


# =====================================
# تست
# =====================================
if __name__ == "__main__":
    print("="*70)
    print("🔥 HYBRID BACKLINK ANALYZER V2")
    print("="*70)
    print("\nمنابع موجود:")
    print("  ✅ SE Ranking API")
    if SELENIUMBASE_AVAILABLE:
        print("  ✅ Ahrefs (SeleniumBase UC mode)")
    else:
        print("  ❌ Ahrefs (نصب کنید: pip install seleniumbase)")
    print("="*70 + "\n")
    
    domain = input("🔑 دامنه: ").strip() or "example.com"
    
    use_ahrefs = input("🦊 استفاده از Ahrefs? (y/n) [y]: ").strip().lower()
    use_ahrefs = use_ahrefs != 'n'
    
    # تست
    analyzer = HybridBacklinkAnalyzerV2(
        prefer_ahrefs=use_ahrefs,
        use_seleniumbase=use_ahrefs,
        headless=False
    )
    
    backlinks = analyzer.fetch_links(domain, limit=50, fallback=True)
    
    print(f"\n{'='*70}")
    print(f"📊 نتیجه: {len(backlinks)} بک‌لینک")
    print("="*70)
    
    if backlinks:
        print("\n✅ نمونه:")
        for i, link in enumerate(backlinks[:5], 1):
            print(f"\n{i}. {link.get('url_from', 'N/A')}")
            print(f"   Anchor: {link.get('anchor', 'N/A')[:50]}")
            print(f"   Source: {link.get('source', 'N/A')}")
            print(f"   Quality Score: {link.get('quality_score', 0):.1f}")
