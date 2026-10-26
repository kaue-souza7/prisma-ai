import React from 'react'

type Block =
  | { type: 'paragraph'; text: string }
  | { type: 'list'; ordered: boolean; items: string[] }
  | { type: 'heading'; level: 3 | 4; text: string }

function parseBlocks(text: string): Block[] {
  const blocks: Block[] = []
  let paragraph: string[] = []
  let list: { ordered: boolean; items: string[] } | null = null

  function flush() {
    if (paragraph.length) {
      blocks.push({ type: 'paragraph', text: paragraph.join(' ') })
      paragraph = []
    }
    if (list) {
      blocks.push({ type: 'list', ordered: list.ordered, items: list.items })
      list = null
    }
  }

  for (const rawLine of text.split('\n')) {
    const line = rawLine.trim()
    if (!line) {
      flush()
      continue
    }

    const heading = line.match(/^(#{3,4})\s+(.*)$/)
    if (heading) {
      flush()
      blocks.push({
        type: 'heading',
        level: heading[1].length === 3 ? 3 : 4,
        text: heading[2],
      })
      continue
    }

    const bullet = line.match(/^[-*]\s+(.*)$/)
    if (bullet) {
      if (paragraph.length) flush()
      if (!list || list.ordered) {
        if (list) blockList(blocks, list)
        list = { ordered: false, items: [] }
      }
      list.items.push(bullet[1])
      continue
    }

    const numbered = line.match(/^\d+\.\s+(.*)$/)
    if (numbered) {
      if (paragraph.length) flush()
      if (!list || !list.ordered) {
        if (list) blockList(blocks, list)
        list = { ordered: true, items: [] }
      }
      list.items.push(numbered[1])
      continue
    }

    if (list) {
      blockList(blocks, list)
      list = null
    }
    paragraph.push(line)
  }

  flush()
  return blocks
}

function blockList(blocks: Block[], list: { ordered: boolean; items: string[] }) {
  blocks.push({ type: 'list', ordered: list.ordered, items: list.items })
}

function renderInline(text: string): React.ReactNode[] {
  return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g).map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('*') && part.endsWith('*')) {
      return <em key={index}>{part.slice(1, -1)}</em>
    }
    return <React.Fragment key={index}>{part}</React.Fragment>
  })
}

export function RichText({ text, className }: { text: string; className?: string }) {
  const blocks = parseBlocks(text)

  return (
    <div className={className}>
      {blocks.map((block, index) => {
        if (block.type === 'heading') {
          return block.level === 3 ? (
            <h3 key={index}>{renderInline(block.text)}</h3>
          ) : (
            <h4 key={index}>{renderInline(block.text)}</h4>
          )
        }
        if (block.type === 'list') {
          const List = block.ordered ? 'ol' : 'ul'
          return (
            <List key={index}>
              {block.items.map((item, itemIndex) => (
                <li key={itemIndex}>{renderInline(item)}</li>
              ))}
            </List>
          )
        }
        return <p key={index}>{renderInline(block.text)}</p>
      })}
    </div>
  )
}
