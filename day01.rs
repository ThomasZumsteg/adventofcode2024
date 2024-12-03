use std::collections::HashMap;
use common::get_input;

type Input = (Vec<usize>, Vec<usize>);

fn part1(rows: &Input) -> usize {
    let mut rows = rows.clone();
    rows.0.sort();
    rows.1.sort();
    rows.0.iter()
        .zip(rows.1.iter())
        .map(|(&a, &b)| {if a > b {a - b} else {b - a}})
        .sum()
}

fn part2(rows: &Input) -> usize {
    let mut counts = HashMap::new();
    rows.1.iter().for_each(|&value| {
        let count = counts.entry(value).or_insert(0);
        *count += 1;
    });
    rows.0.iter()
        .map(|n| n * counts.get(n).unwrap_or(&0))
        .sum()
}

fn parse(text: String) -> Input {
    let mut left = Vec::new();
    let mut right = Vec::new();
    text.split("\n")
        .filter(|line| !line.trim().is_empty())
        .for_each(|line| {
            let values: Vec<usize> = line.trim()
                .split_whitespace()
                .map(|int| int.parse::<usize>().unwrap())
                .collect();
            assert_eq!(values.len(), 2);
            left.push(values[0]);
            right.push(values[1]);
        });
    (left, right)
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEXT: &str = r#"
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    "#;

    #[test]
    fn test_part1() {
        let rows = parse(TEXT.to_string());
        assert_eq!(part1(&rows), 11);
    }

    #[test]
    fn test_part2() {
        let rows = parse(TEXT.to_string());
        assert_eq!(part2(&rows), 31);
    }
}


fn main() {
    let input = parse(get_input(01, 2024));
    println!("Part 1: {}", part1(&input));
    println!("Part 2: {}", part2(&input));
}
