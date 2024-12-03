use common::get_input;

type Input = Vec<Vec<usize>>;

fn safe(report: &Vec<usize>) -> bool {
    let mut count_down: Option<bool> = None;
    for (a, b) in report.iter().zip(report.iter().skip(1)) {
        let mut a = *a;
        let mut b = *b;
        if count_down.is_none() {count_down = Some(a > b)};
        if count_down == Some(false) {
            (b, a) = (a, b);
        }
        if a <= b {
            return false;
        }
        if !(0 < a - b && a - b <= 3) {
            return false;
        }
    }
    true
}

fn part1(reports: &Input) -> usize {
    reports.iter().filter(|report| safe(report)).count()
}

fn part2(reports: &Input) -> usize {
    reports.iter().filter(|report| {
        if safe(report) { return true }
        return (0..report.len()).any(|i| {
            let mut report = (*report).clone();
            report.remove(i);
            safe(&report)
        })
    }).count()
}

fn parse(text: String) -> Input {
    text.split("\n")
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            line.trim()
                .split_whitespace()
                .map(|int| int.parse::<usize>().unwrap())
                .collect()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEXT: &str = r#"7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"#;

    #[test]
    fn test_part1() {
        let input = parse(TEXT.to_string());
        assert_eq!(part1(&input), 2);
    }

    #[test]
    fn test_part2() {
        let input = parse(TEXT.to_string());
        assert_eq!(part2(&input), 4);
    }
}

fn main() {
    let input = parse(get_input(02, 2024));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
