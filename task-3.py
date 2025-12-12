import timeit
import os


# Функція таблиці зсувів для Боєра-Мура ()"""
def build_shift_table(pattern):
    
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


# Алгоритм Боєра-Мура
def boyer_moore_search(text, pattern):
    
    shift_table = build_shift_table(pattern)
    n = len(text)
    m = len(pattern)
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        else:
            shift = shift_table.get(text[i + m - 1], m)
            i += shift
    return -1


# Алгоритм Кнута-Морріса-Пратта (KMP)
def kmp_search(text, pattern):
    
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# Алгоритм Рабіна-Карпа
def rabin_karp_search(text, pattern):
    
    d = 256
    q = 101
    n = len(text)
    m = len(pattern)
    h = 1
    p = 0
    t = 0

    if m > n: return -1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1

# Функція читання файлу
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Якщо не вийшло UTF-8, пробуємо Windows-1251
        try:
            with open(filename, 'r', encoding='cp1251') as f:
                return f.read()
        except Exception as e:
            print(f"Помилка кодування файлу {filename}: {e}")
            return None
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
        return None


if __name__ == "__main__":

# Основна функція тестування
    files_data = [
        {
            "filename": "стаття 1.txt",
            "real_sub": "алгоритм", 
            "fake_sub": "мікрохвильовка"
        },
        {
            "filename": "стаття 2.txt",
            "real_sub": "рекомендац", 
            "fake_sub": "динозавр"
        }
    ]

    results_markdown = []

    for item in files_data:
        text = read_file(item["filename"])
        if not text: continue
        
        print(f"\nОбробка файлу: {item['filename']} (Довжина: {len(text)} символів)")
        print(f"Підрядки: '{item['real_sub']}' (існує), '{item['fake_sub']}' (вигаданий)")
        
        algos = [
            ("Boyer-Moore", boyer_moore_search),
            ("KMP", kmp_search),
            ("Rabin-Karp", rabin_karp_search)
        ]
        
        file_results = {}
        
        for name, func in algos:
            # Вимірюємо час: 100 повторень для кожного пошуку
            t_exist = timeit.timeit(lambda: func(text, item['real_sub']), number=100)
            t_fake = timeit.timeit(lambda: func(text, item['fake_sub']), number=100)
            total_time = t_exist + t_fake
            file_results[name] = total_time
            print(f"  -> {name}: {total_time:.5f} сек")

        fastest = min(file_results, key=file_results.get)
        results_markdown.append({
            "file": item["filename"],
            "times": file_results,
            "fastest": fastest
        })

    # Порядок алгоритмів з першого результату
    algo_names = list(results_markdown[0]["times"].keys())
    
    for name in algo_names:
        t1 = results_markdown[0]["times"][name]
        t2 = results_markdown[1]["times"][name]
        print(f"| {name} | {t1:.5f} | {t2:.5f} |")
    
    print("\nНайшвидші алгоритми:")
    for res in results_markdown:
        print(f"- Для '{res['file']}': **{res['fastest']}**")
